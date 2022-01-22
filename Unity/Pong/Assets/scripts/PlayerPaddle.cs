using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PlayerPaddle : Paddle
{

    private Vector2 _direction;

    private void Update()
    {
        if (Input.GetKey(KeyCode.W) || Input.GetKey(KeyCode.UpArrow))
        {
            _direction = Vector2.up;        // upd in y direction
        }
        else if (Input.GetKey(KeyCode.S) || Input.GetKey(KeyCode.DownArrow))
        {
            _direction = Vector2.down;      // down in y direction
        }
        else
        {
            _direction = Vector2.zero;      //0 values, so nowhere
        }
    }


    private void FixedUpdate()
    {
        if (_direction.sqrMagnitude != 0)
        {
            _rigidbody.AddForce(_direction * speed);
        }
    }



}
