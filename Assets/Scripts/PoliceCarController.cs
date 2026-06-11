using UnityEngine;
using UnityEngine.InputSystem;

public class PoliceCarController : MonoBehaviour
{
    public float speed = 5f;

    void Update()
    {
        // F key -> move left (negative X)
        if (Keyboard.current.fKey.isPressed)
        {
            transform.position += Vector3.left * speed * Time.deltaTime;
        }

        // G key -> move right (positive X)
        if (Keyboard.current.gKey.isPressed)
        {
            transform.position += Vector3.right * speed * Time.deltaTime;
        }
    }
}