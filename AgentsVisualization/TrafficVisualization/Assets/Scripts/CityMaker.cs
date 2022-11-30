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

    Transform reed;
    
    




    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);

        



        // redLight.enabled = !redLight.enabled;





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
        Light();


    }




    // Update is called once per frame
    void Update()
    {

        
        
        
        
        // redLight = GameObject.Find("red");
        // Debug.Log(redLight);
        // semaphorePrefab.transform.Find("red");

        // myRedLight.enabled = !myRedLight.enabled;
        // sema = gameObject.transform.Find("semaphore 1");

        // sema.transform.Find("red").GetComponentInChildren<Light>().enabled = false;
        
    }

    IEnumerator seconds()
    {
        yield return new WaitForSeconds(2);
    }

    void Light()
    {
        semaphorePrefab.transform.Find("Red").gameObject.SetActive(true);
        semaphorePrefab.transform.Find("Green").gameObject.SetActive(false);
        StartCoroutine(seconds());
        semaphorePrefab.transform.Find("Red").gameObject.SetActive(false);
        semaphorePrefab.transform.Find("Green").gameObject.SetActive(false);
        StartCoroutine(seconds());
    }



    void MakeTiles(string tiles)
    {
        int x = 0;
        // Mesa has y 0 at the bottom
        // To draw from the top, find the rows of the file
        // and move down
        // Remove the last enter, and one more to start at 0
        int y = tiles.Split('\n').Length - 1;
       // Debug.Log(y);

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
}    

