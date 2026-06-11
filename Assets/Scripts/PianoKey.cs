using UnityEngine;
using System.Collections;
using System.Text;
using UnityEngine.Networking;

public class PianoKey : MonoBehaviour
{
    [Header("Visual")]
    public float pressDepth = 0.05f;
    public float returnSpeed = 10f;
    public Color postSuccessColor = Color.green;
    public Color postFailureColor = Color.red;
    public float postFeedbackSeconds = 0.25f;

    private Vector3 startPos;
    private bool isPressed;
    private Renderer keyRenderer;
    private Color originalColor;

    [Header("Note")]
    public int noteIndex;

    [Header("Wwise")]
    public AK.Wwise.Event keyEvent;

    [Header("REST API")]
    public bool sendNotesToApi = true;
    public string apiBaseUrl = "http://192.168.1.104:8000";
    public string sessionId = "test-session";

    [System.Serializable]
    private class NotePayload
    {
        public string note;
    }

    void Start()
    {
        startPos = transform.localPosition;
        keyRenderer = GetComponent<Renderer>();

        if (keyRenderer != null)
        {
            originalColor = keyRenderer.material.color;
        }
    }

    void Update()
    {
        Vector3 target = isPressed
            ? startPos - new Vector3(0, pressDepth, 0)
            : startPos;

        transform.localPosition = Vector3.Lerp(
            transform.localPosition,
            target,
            Time.deltaTime * returnSpeed
        );
    }

    // -------------------
    // INTERACTION API
    // -------------------

    public void Press()
    {
        Debug.Log("Key pressed");
        if (isPressed) return;

        isPressed = true;

        // Set which note should be played
        AkSoundEngine.SetRTPCValue(
            "NoteIndex",
            noteIndex,
            gameObject
        );

        Debug.Log($"Playing note {noteIndex}");

        // Trigger Wwise event
        keyEvent.Post(gameObject);

        if (sendNotesToApi)
        {
            StartCoroutine(SendNoteToApi(noteIndex));
        }
    }

    public void Release()
    {
        isPressed = false;
    }

    // -------------------
    // TEST INPUT (mouse)
    // -------------------

    void OnMouseDown()
    {
        Press();
    }

    void OnMouseUp()
    {
        Release();
    }

    private IEnumerator SendNoteToApi(int playedNoteIndex)
    {
        string url = $"{apiBaseUrl}/telemetry/piano-note";

        NotePayload payload = new NotePayload
        {
            note = playedNoteIndex.ToString()
        };

        string json = JsonUtility.ToJson(payload);
        Debug.Log($"Sending note {playedNoteIndex} to API: {url}");

        using UnityWebRequest request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogWarning(
                $"Failed to send note {playedNoteIndex}: {request.responseCode} {request.error} {request.downloadHandler.text}"
            );
            StartCoroutine(ShowPostFeedback(postFailureColor));
        }
        else
        {
            Debug.Log($"Sent note {playedNoteIndex} to API: {url}");
            StartCoroutine(ShowPostFeedback(postSuccessColor));
        }
    }

    private IEnumerator ShowPostFeedback(Color color)
    {
        if (keyRenderer == null)
        {
            yield break;
        }

        keyRenderer.material.color = color;
        yield return new WaitForSeconds(postFeedbackSeconds);
        keyRenderer.material.color = originalColor;
    }
}
