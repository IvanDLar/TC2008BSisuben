using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; 
using TMPro;


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
    [SerializeField] GameObject buildingPrefab1;
    [SerializeField] GameObject buildingPrefab;
    [SerializeField] GameObject buildingPrefab2;
    [SerializeField] GameObject buildingPrefab3;
    [SerializeField] GameObject semaphorePrefab;
    [SerializeField] GameObject parkingPrefab;
    [SerializeField] int tileSize;

    List<GameObject> prefabList = new List <GameObject>();
    List<GameObject> Semaphore_s = new List <GameObject>();
    List<GameObject> Semaphore_S = new List <GameObject>();
    
    bool state = false;

    public TextMeshPro  textvalue;
    
    private GameObject[] getCount;

    int count;
    




    // Start is called before the first frame update
    void Start()
    {
        MakeTiles(layout.text);


    

    }




    // Update is called once per frame
    void Update()
    {

        getCount = GameObject.FindGameObjectsWithTag ("Car");
        count = getCount.Length;
        textvalue.text = count.ToString();
        
    }

    IEnumerator seconds()
    {
        yield return new WaitForSeconds(20);
    }

    void Light_s(GameObject sem, bool state)
    {
        sem.transform.Find("Red").gameObject.SetActive(state);
        sem.transform.Find("Green").gameObject.SetActive(!state);
    }

    public void switchLight()
    {

        foreach(var sem in Semaphore_s)
        {
            Light_s(sem, state);
            
        }

        foreach(var sem in Semaphore_S)
        {
            Light_s(sem, !state);
        }

        state = !state;
    }




    void MakeTiles(string tiles)
    {
        int x = 0;
        prefabList.Add(buildingPrefab1);
        prefabList.Add(buildingPrefab);
        prefabList.Add(buildingPrefab2);
        prefabList.Add(buildingPrefab3);
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
                Light_s(tile, true);
                Semaphore_s.Add(tile);
                tile.transform.parent = transform;
                x += 1;
                
            } else if (tiles[i] == 'S') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(roadPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.transform.parent = transform;
                tile = Instantiate(semaphorePrefab, position, Quaternion.Euler(0, 90, 0));
                Light_s(tile, false);
                Semaphore_S.Add(tile);
                tile.transform.parent = transform;
                x += 1;
                
            } else if (tiles[i] == 'D') {
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(parkingPrefab, position, Quaternion.Euler(0, 90, 0));
                tile.GetComponent<Renderer>().materials[1].color = Color.red;
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '#') {
                int prefabIndex = UnityEngine.Random.Range(0,4);
                position = new Vector3(x * tileSize, 0, y * tileSize);
                tile = Instantiate(prefabList[prefabIndex], position, Quaternion.identity);
                // tile.transform.localScale = new Vector3(1, Random.Range(0.5f, 2.0f), 1);
                tile.transform.parent = transform;
                x += 1;
            } else if (tiles[i] == '\n') {
                x = 0;
                y -= 1;
            }
        }

    }
}    

