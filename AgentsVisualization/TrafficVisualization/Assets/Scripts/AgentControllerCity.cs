// TC2008B. Sistemas Multiagentes y Gráficas Computacionales
// C# client to interact with Python. Based on the code provided by Sergio Ruiz.
// Octavio Navarro. October 2021

using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor;
using UnityEngine;
using UnityEngine.Networking;

// [Serializable]
// public class AgentData2
// {
//     public string id;
//     public float x, y, z;

//     public AgentData2(string id, float x, float y, float z)
//     {
//         this.id = id;
//         this.x = x;
//         this.y = y;
//         this.z = z;
//     }
// }

// [Serializable]

// public class AgentsData2
// {
//     public List<AgentData> positions;

//     public AgentsData2() => this.positions = new List<AgentData2>();
// }

public class AgentControllerCity : MonoBehaviour
{
    // private string url = "https://agents.us-south.cf.appdomain.cloud/";
    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    AgentsData agentsData;
    Dictionary<string, GameObject> agents;
    Dictionary<string, Vector3> prevPositions, currPositions;

    bool updated = false, started = false;

    public GameObject [] prefabList;
    public int NAgents;
    public float timeToUpdate = 5.0f;
    private float timer, dt;
    int stepCounter = 0;


    public GameObject City;

    CityMaker citymaker;



    void Start()
    {
        citymaker = City.GetComponent<CityMaker>();

        agentsData = new AgentsData();

        prevPositions = new Dictionary<string, Vector3>();
        currPositions = new Dictionary<string, Vector3>();

        agents = new Dictionary<string, GameObject>(); //Car agent lists 
        
        timer = timeToUpdate;

        StartCoroutine(SendConfiguration());
    }

    void newCar(string id, Vector3 newAgentPosition){
        int prefabIndex = UnityEngine.Random.Range(0,prefabList.Length);
        prevPositions[id] = newAgentPosition;
        agents[id] = Instantiate(prefabList[prefabIndex], newAgentPosition, Quaternion.identity);
    }

    private void Update() 
    {
    
        if(timer < 0)
        {
            timer = timeToUpdate;
            updated = false;
            StartCoroutine(UpdateSimulation());
            stepCounter++;
            if(stepCounter % 10 == 0)
            {
                citymaker.switchLight();
            }
        }

        if (updated)
        {
            
            timer -= Time.deltaTime;
            dt = 1.0f - (timer / timeToUpdate);

            foreach(var agent in currPositions)
            {
                Vector3 currentPosition = agent.Value;

                if(!prevPositions.ContainsKey(agent.Key)){
                    newCar(agent.Key, currentPosition);
                }

                Vector3 previousPosition = prevPositions[agent.Key];

                Vector3 interpolated = Vector3.Lerp(previousPosition, currentPosition, dt);
                Vector3 direction = currentPosition - interpolated;

                agents[agent.Key].transform.localPosition = interpolated;
                if(direction != Vector3.zero) agents[agent.Key].transform.rotation = Quaternion.LookRotation(direction);
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
        }
    }

    IEnumerator SendConfiguration()
    {
        WWWForm form = new WWWForm();

        form.AddField("NAgents", NAgents.ToString());

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

            Debug.Log(www.downloadHandler.text);
            foreach(AgentData agent in agentsData.positions)
            {
                Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);

                    if(!started)
                    {

                        newCar(agent.id, newAgentPosition);
                    }
                    else
                    {
                        Vector3 currentPosition = new Vector3();
                        if(currPositions.TryGetValue(agent.id, out currentPosition))
                            prevPositions[agent.id] = currentPosition;
                        currPositions[agent.id] = newAgentPosition;
                        
                    }
            }

            updated = true;
            if(!started) started = true;
        }
    }

}