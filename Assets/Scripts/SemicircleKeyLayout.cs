using UnityEngine;

public class SemicircleKeyLayout : MonoBehaviour
{
    public GameObject keyPrefab;
    public bool createOnStart = false;
    // public string apiBaseUrl = "http://153.19.215.83:8000";
    public string apiBaseUrl = "http://192.168.1.104:8000";

    public float radius = 3f;

    public float offsetX = 0f;
    public float offsetZ = 1f;

    public float yPosition = 0f;

    float[] angles = { -63f, -45f, -27f, -9f, 9f, 27f, 45f, 63f };

    void Start()
    {
        if (createOnStart)
        {
            CreateKeys("assessment");
        }
    }

    public void CreateKeys(string taskType)
    {
        ClearKeys();

        float angleOffset = GetAngleOffset(taskType);

        for (int i = 0; i < angles.Length; i++)
        {
            float angle = angles[i] + angleOffset;
            float rad = angle * Mathf.Deg2Rad;

            float x = Mathf.Sin(rad) * radius + offsetX;
            float z = Mathf.Cos(rad) * radius + offsetZ;

            Vector3 pos = new Vector3(x, yPosition, z);

            GameObject key = Instantiate(keyPrefab, pos, Quaternion.identity, transform);

            PianoKey pianoKey = key.GetComponent<PianoKey>();

            if (pianoKey != null)
            {
                pianoKey.noteIndex = i;
                pianoKey.apiBaseUrl = apiBaseUrl;
            }

            key.transform.rotation = Quaternion.Euler(-45f, angle, 0f);
        }
    }

    private float GetAngleOffset(string taskType)
    {
        if (taskType == "scales")
        {
            return -20f;
        }

        return 0f;
    }

    private void ClearKeys()
    {
        for (int i = transform.childCount - 1; i >= 0; i--)
        {
            Destroy(transform.GetChild(i).gameObject);
        }
    }
}
