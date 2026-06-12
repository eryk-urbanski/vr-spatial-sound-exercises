using UnityEngine;
using System.Collections;
using System.Text;
using UnityEngine.Networking;

public class HeadRotationTelemetry : MonoBehaviour
{
    // public string apiBaseUrl = "http://153.19.215.83:8000";
    public string apiBaseUrl = "http://192.168.1.104:8000";
    public Transform headTransform;
    public float sendIntervalSeconds = 0.5f;
    public bool sendTelemetry = false;

    [System.Serializable]
    private class HeadRotationPayload
    {
        public float angle_degrees;
    }

    void Start()
    {
        if (headTransform == null && Camera.main != null)
        {
            headTransform = Camera.main.transform;
        }

        StartCoroutine(SendHeadRotationLoop());
    }

    private IEnumerator SendHeadRotationLoop()
    {
        while (true)
        {
            if (sendTelemetry && headTransform != null)
            {
                yield return SendHeadRotationToApi();
            }

            yield return new WaitForSeconds(sendIntervalSeconds);
        }
    }

    private IEnumerator SendHeadRotationToApi()
    {
        string url = $"{apiBaseUrl}/telemetry/head-position";

        HeadRotationPayload payload = new HeadRotationPayload
        {
            angle_degrees = NormalizeAngle(headTransform.eulerAngles.y)
        };

        string json = JsonUtility.ToJson(payload);
        Debug.Log($"Sending head rotation {payload.angle_degrees} to API: {url}");

        using UnityWebRequest request = new UnityWebRequest(url, "POST");
        byte[] bodyRaw = Encoding.UTF8.GetBytes(json);

        request.uploadHandler = new UploadHandlerRaw(bodyRaw);
        request.downloadHandler = new DownloadHandlerBuffer();
        request.SetRequestHeader("Content-Type", "application/json");

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success)
        {
            Debug.LogWarning(
                $"Failed to send head rotation: {request.responseCode} {request.error} {request.downloadHandler.text}"
            );
        }
    }

    private float NormalizeAngle(float angle)
    {
        if (angle > 180f)
        {
            return angle - 360f;
        }

        return angle;
    }
}
