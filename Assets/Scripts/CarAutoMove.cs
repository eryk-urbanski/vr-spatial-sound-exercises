using UnityEngine;
using UnityEngine.InputSystem;

public class CarAutoMove : MonoBehaviour
{
    public Transform target;
    public Transform startPoint;
    public float speed = 5f;

    private bool isMoving = true;

    void Start()
    {
        if (startPoint != null)
            transform.position = startPoint.position;
    }

    void Update()
    {
        // R key using NEW Input System
        if (Keyboard.current.rKey.wasPressedThisFrame)
        {
            ResetCar();
        }

        if (!isMoving || target == null) return;

        transform.position = Vector3.MoveTowards(
            transform.position,
            target.position,
            speed * Time.deltaTime
        );

        if (Vector3.Distance(transform.position, target.position) < 0.1f)
        {
            isMoving = false;
        }
    }

    void ResetCar()
    {
        if (startPoint != null)
            transform.position = startPoint.position;

        isMoving = true;
    }
}