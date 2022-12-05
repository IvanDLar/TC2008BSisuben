using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Camaras : MonoBehaviour
{
    public GameObject [] Cams;
    int index = 0;
    // Start is called before the first frame update
    void Start()
    {
        InvokeRepeating("proyectCamaras",10,10);
    }

    // Update is called once per frame
    void proyectCamaras()
    {
        Cams[index].SetActive(false);
        index = (index+1) %Cams.Length;
        Cams[index].SetActive(true);

        
    }
}
