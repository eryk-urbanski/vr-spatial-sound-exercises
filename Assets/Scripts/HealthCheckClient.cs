using UnityEngine;
using UnityEngine.Networking;
using System.Collections;

public class HealthCheckClient : MonoBehaviour
{
    private void Start()
    {
        StartCoroutine(CheckHealth());
    }

    private IEnumerator CheckHealth()
    {
        UnityWebRequest request = UnityWebRequest.Get("http://localhost:8000/health");
        yield return request.SendWebRequest();

        if (request.result == UnityWebRequest.Result.Success)
        {
            Debug.Log("Health Check Successful: " + request.downloadHandler.text);
        }
        else
        {
            Debug.LogError("Health Check Failed: " + request.error);
        }
    }
}
