using UnityEngine;
using UnityEngine.InputSystem;

public class MousePointerRay : MonoBehaviour
{
    public float range = 10f;

    void Update()
    {
        if (Mouse.current == null) return;

        Vector2 mousePos = Mouse.current.position.ReadValue();
        Ray ray = Camera.main.ScreenPointToRay(mousePos);

        if (Physics.Raycast(ray, out RaycastHit hit, range))
        {
            Debug.DrawLine(ray.origin, hit.point, Color.green);

            if (Mouse.current.leftButton.wasPressedThisFrame)
            {
                var key = hit.collider.GetComponent<PianoKey>();
                if (key != null)
                {
                    key.Press();
                }
            }
        }
    }
}