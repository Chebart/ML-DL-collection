using System.Collections;
using System.Collections.Generic;
using System.Linq;
using UnityEngine;
using System.Threading;

public class PointsAnimation2 : MonoBehaviour
{

    public GameObject[] Animpoints;
    List<string> lines;
    float x, y, z;
    int counter = 0;
    // Start is called before the first frame update
    void Start()
    {
        lines = System.IO.File.ReadLines("Assets/Animation2.txt").ToList();
    }

    // Update is called once per frame
    void Update()
    {
        string[] points = lines[counter].Split(',');

        for (int i = 0; i < points.Length / 3; i++)
        {
            x = float.Parse(points[0 + (i * 3)]) / 100;
            y = float.Parse(points[1 + (i * 3)]) / 100;
            z = float.Parse(points[2 + (i * 3)]) / 100;
            Animpoints[i].transform.localPosition = new Vector3(x, y, z);
        }

        counter += 1;

        if (counter == lines.Count) { counter = 0; }

        Thread.Sleep(50);
    }
}
