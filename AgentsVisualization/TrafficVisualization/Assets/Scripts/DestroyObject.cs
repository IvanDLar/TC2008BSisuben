using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class DestroyObject : MonoBehaviour
{

void OnCollisionEnter(Collision col)
{
    if (col.gameObject.tag == "Box")
    {
        Destroy(col.gameObject); // <== Remove colliding object
        Debug.Log("yell");
    }
}
}