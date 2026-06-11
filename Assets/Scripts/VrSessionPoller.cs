using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class VrSessionPoller : MonoBehaviour
{
    // public string apiBaseUrl = "http://153.19.215.83:8000";
    public string apiBaseUrl = "http://192.168.1.104:8000";
    public float pollIntervalSeconds = 1f;
    public SemicircleKeyLayout pianoGenerator;
    public HeadRotationTelemetry headRotationTelemetry;

    private int? currentSessionId = null;

    [System.Serializable]
    private class SessionCommand
    {
        public bool should_run;
        public int session_id;
        public string task_type;
    }

    private void Start()
    {
        if (pianoGenerator == null)
        {
            GameObject pianoGeneratorObject = GameObject.Find("PianoGenerator");
            if (pianoGeneratorObject != null)
            {
                pianoGenerator = pianoGeneratorObject.GetComponent<SemicircleKeyLayout>();
            }
        }

        if (pianoGenerator != null)
        {
            pianoGenerator.apiBaseUrl = apiBaseUrl;
        }

        if (headRotationTelemetry == null)
        {
            headRotationTelemetry = FindObjectOfType<HeadRotationTelemetry>();
        }

        if (headRotationTelemetry != null)
        {
            headRotationTelemetry.apiBaseUrl = apiBaseUrl;
        }

        StartCoroutine(PollSessionCommand());
    }

    private IEnumerator PollSessionCommand()
    {
        while (true)
        {
            yield return GetSessionCommand();
            yield return new WaitForSeconds(pollIntervalSeconds);
        }
    }

    private IEnumerator GetSessionCommand()
    {
        string url = $"{apiBaseUrl}/vr/session-command";

        using UnityWebRequest request = UnityWebRequest.Get(url);
        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogWarning($"Session command request failed: {request.error}");
            yield break;
        }

        SessionCommand command = JsonUtility.FromJson<SessionCommand>(
            request.downloadHandler.text
        );

        if (!command.should_run)
        {
            if (currentSessionId.HasValue)
            {
                StopCurrentTask();
                currentSessionId = null;
            }

            yield break;
        }

        if (!currentSessionId.HasValue)
        {
            StartTask(command.task_type);
            currentSessionId = command.session_id;
            yield break;
        }

        if (currentSessionId.Value != command.session_id)
        {
            StopCurrentTask();
            StartTask(command.task_type);
            currentSessionId = command.session_id;
        }
    }

    private void StartTask(string taskType)
    {
        Debug.Log($"Starting VR task: {taskType}");
        SetTelemetryEnabled(true);

        if (taskType == "assessment" || taskType == "scales")
        {
            StartPianoTask(taskType);
        }
    }

    private void StartPianoTask(string taskType)
    {
        if (pianoGenerator == null)
        {
            Debug.LogWarning("PianoGenerator with SemicircleKeyLayout was not found.");
            return;
        }

        pianoGenerator.CreateKeys(taskType);
    }

    private void StopCurrentTask()
    {
        Debug.Log("Stopping current VR task");
        SetTelemetryEnabled(false);

        // TODO:
        // disable current task objects here
    }

    private void SetTelemetryEnabled(bool enabled)
    {
        if (headRotationTelemetry != null)
        {
            headRotationTelemetry.sendTelemetry = enabled;
        }
    }
}
