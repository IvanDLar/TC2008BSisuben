﻿// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

[Serializable]
public class AgentData
{
    public string id;
    public float x, y, z;

    public AgentData(string id, float x, float y, float z)
    {
        this.id = id;
        this.x = x;
        this.y = y;
        this.z = z;
    }
}

[Serializable]

public class AgentsData
{
    public List<AgentData> positions;

    public AgentsData() => this.positions = new List<AgentData>();
}

public class AgentController : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getBoxesEndpoint = "/getBoxes";
    string getObstaclesEndpoint = "/getObstacles";
    string getEndpointsEndpoint = "/getEndPoints";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData, obstacleData, boxData, endPointData;
    Dictionary<string, GameObject> agents, boxes;
    Dictionary<string, Vector3> prevPositions, currPositions, prevBoxPositions, currBoxPositions;

    bool updated = false, started = false;

    public GameObject agentPrefab, obstaclePrefab, boxPrefab, endPointPrefab, floor;
    public int NAgents, NBoxes, NEndPoints, width, height;
    public float timeToUpdate = 5.0f;
    private float timer, dt;

    void Start()
    {
        agentsData = new AgentsData();
        obstacleData = new AgentsData();
        endPointData = new AgentsData();
        boxData = new AgentsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        prevBoxPositions = new Dictionary<string, Vector3>();
        currBoxPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>();
        boxes = new Dictionary<string, GameObject>();

        floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    private void Update() 
    {
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
        }

        if (updated)
        {
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;
                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
            }
            foreach(var box in currBoxPositions)
            {
                Vector3 currentBoxPosition = box.Value;
                Vector3 previousBoxPosition = prevBoxPositions[box.Key];

                Vector3 interpolatedBox = Vector3.Lerp(previousBoxPosition, currentBoxPosition, dt);
                Vector3 direction = currentBoxPosition - interpolatedBox;

                boxes[box.Key].transform.localPosition = interpolatedBox;
                if(direction != Vector3.zero) boxes[box.Key].transform.rotation = Quaternion.LookRotation(direction);
            }

            // float t = (timer / timeToUpdate);
            // dt = t * t * ( 3f - 2f*t);
        }
    }
 
    IEnumerator UpdateSimulation()
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetBoxData()); 
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());
        form.AddField("NBoxes", NBoxes.ToString());
        form.AddField("NEndPoints", NEndPoints.ToString());
        form.AddField("width", width.ToString());
        form.AddField("height", height.ToString());

        UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
        www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

        yield return www.SendWebRequest();

        if (www.result != UnityWebRequest.Result.Success)
        {
            Debug.Log(www.error);
        }
        else
        {
            Debug.Log("Configuration upload complete!");
            Debug.Log("Getting Agents positions");
            StartCoroutine(GetAgentsData());
            StartCoroutine(GetObstacleData());
            StartCoroutine(GetBoxData());
            StartCoroutine(GetEndPointData());
        }
    }

    IEnumerator GetAgentsData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            foreach(AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);

                    if(!started)
                    {
                        prevPositions[agent.id] = newAgentPosition;
                        agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;
                    }
            }

            //updated = true;
            //if(!started) started = true;
        }
    }

    IEnumerator GetObstacleData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            obstacleData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(obstacleData.positions);

            foreach(AgentData obstacle in obstacleData.positions)
            {
                Instantiate(obstaclePrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
            }
        }
    }
    IEnumerator GetBoxData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBoxesEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            boxData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);
            
            foreach(AgentData box in boxData.positions)
            {
                Vector3 newBoxPosition = new Vector3(box.x, box.y, box.z);

                    if(!started)
                    {
                        prevBoxPositions[box.id] = newBoxPosition;
                        boxes[box.id] = Instantiate(boxPrefab, newBoxPosition, Quaternion.identity);
                    }
                    else
                    {
                        //Compara los JSONS, si falta alguna de las cajas en el nuevo JSON eliminar la caja de unity

                        // Vector3 currentBoxPosition = new Vector3();
                        // if(currBoxPositions.TryGetValue(box.id, out currentBoxPosition))
                        //     prevBoxPositions[box.id] = currentBoxPosition;
                        // currBoxPositions[box.id] = newBoxPosition;
                    }
            }

            updated = true;
            if(!started) started = true;
        }
    }

    IEnumerator GetEndPointData() 
    {
        UnityWebRequest www = UnityWebRequest.Get(serverUrl + getEndpointsEndpoint);
        yield return www.SendWebRequest();
 
        if (www.result != UnityWebRequest.Result.Success)
            Debug.Log(www.error);
        else 
        {
            endPointData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

            Debug.Log(endPointData.positions);

            foreach(AgentData endPoint in endPointData.positions)
            {
                Instantiate(endPointPrefab, new Vector3(endPoint.x, endPoint.y, endPoint.z), Quaternion.identity);
            }
        }
    }
}