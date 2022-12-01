using System.Collections;
using System.Collections.Generic;
using UnityEngine;


// public class AgentData
// {
//     public string id;
//     public float x, y, z;

//     public AgentData(string id, float x, float y, float z)
//     {
//         this.id = id;
//         this.x = x;
//         this.y = y;
//         this.z = z;
//     }
// }

// [Serializable]

// public class AgentsData
// {
//     public List<AgentData> positions;

//     public AgentsData() => this.positions = new List<AgentData>();
// }

public class CityMaker : MonoBehaviour
{
    [SerializeField] TextAsset layout;
    [SerializeField] GameObject roadPrefab;
    [SerializeField] GameObject buildingPrefab;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] int tileSize;

    string serverUrl = "http://localhost:8585";
    string getAgentsEndpoint = "/getAgents";
    string getObstaclesEndpoint = "/getObstacles";
    string getEndpointsEndpoint = "/getEndPoints";
    string sendConfigEndpoint = "/init";
    string updateEndpoint = "/update";
    




    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);

        // var textFile = Resources.Load<GameObject>("Assets/Prefabs/semaphore 1");

        // semaphorePrefab = GameObject.Find("red");
        // myRedLight = redLight.GetComponentInChildren<Light>();

        // agentsData = new AgentsData();
        // obstacleData = new AgentsData();
        // endPointData = new AgentsData();

        // prevPositions = new Dictionary<string, Vector3>();
        // currPositions = new Dictionary<string, Vector3>();

        // // prevBoxPositions = new Dictionary<string, Vector3>();
        // // currBoxPositions = new Dictionary<string, Vector3>();

        // agents = new Dictionary<string, GameObject>();
        // // boxes = new Dictionary<string, GameObject>();

        // floor.transform.localScale = new Vector3((float)width/10, 1, (float)height/10);
        // floor.transform.localPosition = new Vector3((float)width/2-0.5f, 0, (float)height/2-0.5f);
        
        // timer = timeToUpdate;

        // StartCoroutine(SendConfiguration());


    }




    // Update is called once per frame
    void Update()
    {
        // myRedLight.enabled = !myRedLight.enabled;
        // sema = gameObject.transform.Find("semaphore 1");

        // sema.transform.Find("red").GetComponentInChildren<Light>().enabled = false;
        
    }

    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 2;
        Debug.Log(y);

        Vector3 position;
        GameObject tile;

        for (int i=0; i<tiles.Length; i++) {
            if (tiles[i] == '>' || tiles[i] == '<') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'v' || tiles[i] == '^') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 's') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, position, Quaternion.identity);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'S') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.GetComponent<Renderer>().materials[0].color = Color.red;
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(buildingPrefab, position, Quaternion.identity);
                tile.transform.localScale = new Vector3(1, Random.Range(0.5f, 2.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }


    // IEnumerator UpdateSimulation()
    // {
    //     UnityWebRequest www = UnityWebRequest.Get(serverUrl + updateEndpoint);
    //     yield return www.SendWebRequest();
 
    //     if (www.result != UnityWebRequest.Result.Success)
    //         Debug.Log(www.error);
    //     else 
    //     {
    //         StartCoroutine(GetAgentsData());
    //         StartCoroutine(GetBoxData()); 
    //     }
    // }

//     IEnumerator SendConfiguration()
//     {
//         WWWForm form = new WWWForm();

//         form.AddField("NAgents", NAgents.ToString());
//         form.AddField("NBoxes", NBoxes.ToString());
//         form.AddField("NEndPoints", NEndPoints.ToString());
//         form.AddField("width", width.ToString());
//         form.AddField("height", height.ToString());

//         UnityWebRequest www = UnityWebRequest.Post(serverUrl + sendConfigEndpoint, form);
//         www.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded");

//         yield return www.SendWebRequest();

//         if (www.result != UnityWebRequest.Result.Success)
//         {
//             Debug.Log(www.error);
//         }
//         else
//         {
//             Debug.Log("Configuration upload complete!");
//             Debug.Log("Getting Agents positions");
//             StartCoroutine(GetAgentsData());
//             StartCoroutine(GetObstacleData());
//             StartCoroutine(GetBoxData());
//             StartCoroutine(GetEndPointData());
//         }
//     }

//     IEnumerator GetAgentsData() 
//     {
//         UnityWebRequest www = UnityWebRequest.Get(serverUrl + getAgentsEndpoint);
//         yield return www.SendWebRequest();
 
//         if (www.result != UnityWebRequest.Result.Success)
//             Debug.Log(www.error);
//         else 
//         {
//             agentsData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

//             foreach(AgentData agent in agentsData.positions)
//             {
//                 Vector3 newAgentPosition = new Vector3(agent.x, agent.y, agent.z);

//                     if(!started)
//                     {
//                         prevPositions[agent.id] = newAgentPosition;
//                         agents[agent.id] = Instantiate(agentPrefab, newAgentPosition, Quaternion.identity);
//                     }
//                     else
//                     {
//                         Vector3 currentPosition = new Vector3();
//                         if(currPositions.TryGetValue(agent.id, out currentPosition))
//                             prevPositions[agent.id] = currentPosition;
//                         currPositions[agent.id] = newAgentPosition;
//                     }
//             }

//             //updated = true;
//             //if(!started) started = true;
//         }
//     }

//     IEnumerator GetObstacleData() 
//     {
//         UnityWebRequest www = UnityWebRequest.Get(serverUrl + getObstaclesEndpoint);
//         yield return www.SendWebRequest();
 
//         if (www.result != UnityWebRequest.Result.Success)
//             Debug.Log(www.error);
//         else 
//         {
//             obstacleData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

//             Debug.Log(obstacleData.positions);

//             foreach(AgentData obstacle in obstacleData.positions)
//             {
//                 Instantiate(obstaclePrefab, new Vector3(obstacle.x, obstacle.y, obstacle.z), Quaternion.identity);
//             }
//         }
//     }
//     IEnumerator GetBoxData() 
//     {
//         UnityWebRequest www = UnityWebRequest.Get(serverUrl + getBoxesEndpoint);
//         yield return www.SendWebRequest();
 
//         if (www.result != UnityWebRequest.Result.Success)
//             Debug.Log(www.error);
//         else 
//         {
//             boxData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);
            
//             foreach(AgentData box in boxData.positions)
//             {
//                 Vector3 newBoxPosition = new Vector3(box.x, box.y, box.z);

//                     if(!started)
//                     {
//                         prevBoxPositions[box.id] = newBoxPosition;
//                         boxes[box.id] = Instantiate(boxPrefab, newBoxPosition, Quaternion.identity);
//                     }
//                     else
//                     {
//                         //Compara los JSONS, si falta alguna de las cajas en el nuevo JSON eliminar la caja de unity

//                         // Vector3 currentBoxPosition = new Vector3();
//                         // if(currBoxPositions.TryGetValue(box.id, out currentBoxPosition))
//                         //     prevBoxPositions[box.id] = currentBoxPosition;
//                         // currBoxPositions[box.id] = newBoxPosition;
//                     }
//             }

//             updated = true;
//             if(!started) started = true;
//         }
//     }

//     IEnumerator GetEndPointData() 
//     {
//         UnityWebRequest www = UnityWebRequest.Get(serverUrl + getEndpointsEndpoint);
//         yield return www.SendWebRequest();
 
//         if (www.result != UnityWebRequest.Result.Success)
//             Debug.Log(www.error);
//         else 
//         {
//             endPointData = JsonUtility.FromJson<AgentsData>(www.downloadHandler.text);

//             Debug.Log(endPointData.positions);

//             foreach(AgentData endPoint in endPointData.positions)
//             {
//                 Instantiate(endPointPrefab, new Vector3(endPoint.x, endPoint.y, endPoint.z), Quaternion.identity);
//             }
//         }
//     }
}
