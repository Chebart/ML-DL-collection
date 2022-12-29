using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PointsTracking : MonoBehaviour
{
    // Start is called before the first frame update
    public UDPReceive udpReceive;
    public GameObject[] handPoints;
    float x, y, z;
    void Start()
    {

    }

    // Update is called once per frame
    void Update()
    {
        string data = udpReceive.data;
        data = data.Remove(0, 1);
        data = data.Remove(data.Length - 1, 1);
        string[] points = data.Split(',');

        for (int i = 0; i < points.Length / 3; i++)
        {
            x = 7 - float.Parse(points[i * 3 + 0]) / 100;
            y = float.Parse(points[i * 3 + 1]) / 100;
            z = float.Parse(points[i * 3 + 2]) / 100;

            handPoints[i].transform.localPosition = new Vector3(x, y, z);

        }


    }
}