using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Grid : MonoBehaviour
{
    public List<Cell> cells;

    // Start is called before the first frame update
    void Start()
    {
        var cellPrefab = Resources.Load<Cell>("Cell");

        for (int i = 0; i < 9; i++) {
            for (int j = 0; j < 9; j++) {
                var cell = Instantiate(cellPrefab);
                cell.row = i;
                cell.col = j;
                cells.Add(cell);
            }
        }
    }

    // Update is called once per frame
    void Update()
    {
        
    }
}
