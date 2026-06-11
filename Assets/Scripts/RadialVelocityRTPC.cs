using UnityEngine;

public class RadialVelocityRTPC : MonoBehaviour
{
    public Transform listener;

    // Name of RTPC in Wwise
    public string rtpcName = "RadialVelocity";

    private Vector3 previousSourcePosition;
    private Vector3 previousListenerPosition;

    void Start()
    {
        previousSourcePosition = transform.position;
        previousListenerPosition = listener.position;
    }

    void Update()
    {
        float dt = Time.deltaTime;

        if (dt <= 0f) return;

        // Calculate source velocity
        Vector3 sourceVelocity =
            (transform.position - previousSourcePosition) / dt;

        // Calculate listener velocity
        Vector3 listenerVelocity =
            (listener.position - previousListenerPosition) / dt;

        // Relative velocity
        Vector3 relativeVelocity =
            sourceVelocity - listenerVelocity;

        // Direction from listener to source
        Vector3 sourceDirection =
            (transform.position - listener.position).normalized;

        // Radial velocity
        float radialVelocity =
            Vector3.Dot(relativeVelocity, sourceDirection);

        // Send RTPC to Wwise
        AkSoundEngine.SetRTPCValue(
            rtpcName,
            radialVelocity,
            gameObject
        );

        // Store positions for next frame
        previousSourcePosition = transform.position;
        previousListenerPosition = listener.position;
    }
}