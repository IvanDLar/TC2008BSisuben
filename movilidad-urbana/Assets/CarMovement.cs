/*Compute the new position fo an object, using Linear Interpolation (LERP)*/

using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CarMovement : MonoBehaviour
{

    [SerializeField] Vector3 startPos;
    [SerializeField] Vector3 stopPos;

    [SerializeField] float motionTime;

    float currentTime;
    float t;
    float index;

    Vector3 = 
    Vector3[] waypoints = new Vector3[5];

    // Start is called before the first frame update
    void Start()
    {
        waypoints[0] = new Vector3[0,0,0];
        waypoints[1] = new Vector3[0,0,1];
        waypoints[2] = new Vector3[0,0,2];
        waypoints[3] = new Vector3[1,0,3];
        waypoints[4] = new Vector3[2,0,3];

        startPos = waypoints[0];
        stopPos = waypoints[1];
        index = 1;

    }

    // Update is called once per frame
    void Update()
    {
        //SimpleMotion();
        RandomPoints();
    }

    void SimpleMotion(){
        //Transition and mask the animation when animation the objeect
        transform.position = Vector3.Lerp(startPos, stopPos, GetT());
    }

    void RandomPoints(){
        t = GetT();
        transform.position = Vector3.Lerp(startPos, stopPos, t);

        //Generate a new point when reaching the target
        if(t == 1){
            currentTime = 0;
            startPos = waypoints[index];
            index += 1;
            if(index == waypoints.Length){
                index = 0;
            }
            stopPos = waypoints[index];
            // Vector2 displacement = Random.insideUnitCircle * 5;
            // stopPos = new Vector3(startPos.x + displacement.x,
            //                                     0,
            //                                     startPos.z + displacement.y);
        }
        
    }

    void RotateAgent(){
        float radius = 1;
        //Smooth out the angle shift of the object (when turning for example)
        float angle = Mathf.Lerp(Mathf.PI, Math.PI/2, t);
        float x = Mathf.Cos(angle) * radius;
        float y = Mathf.Sin(angle) * radius;
    }

    float GetT(){
        //Tiempo transcurrido desde el ultimo frame
        currentTime += Time.deltaTime;
        t = currentTime / motionTime;

        if (t > 1){
            t = 1;
        }

        return t;
    }
    
}
