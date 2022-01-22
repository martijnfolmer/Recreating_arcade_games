using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Paddle : MonoBehaviour
{
    protected Rigidbody2D _rigidbody;       // protected means this class can access it, and its children can access it
    public float speed = 10.0f;

    private void Awake()        // run on awake, so once in the lifecycle. Usefull for initialization
    {

        _rigidbody = GetComponent<Rigidbody2D>();   // find the ridgidbody component of this instance



    }
}
