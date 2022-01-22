using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Ball : MonoBehaviour
{
    public float speed = 150.0f;
    private Rigidbody2D _rigidBody;

    private void Awake()
    {
        _rigidBody = GetComponent<Rigidbody2D>();
    }

    private void Start()
    {
        ResetPosition();    //initialize speed and such of the ball
    }

    private void AddStartingForce()
    {
        float x = Random.value < 0.5f ? -1.0f : 1.0f;                                           //ternary operaters (either go left or right)
        float y = Random.value < 0.5f ? Random.Range(-1.0f, -0.5f) : Random.Range(0.5f, 1.0f);  // Always give it an angle, either up or down

        Vector2 direction = new Vector2(x, y);
        _rigidBody.AddForce(direction * this.speed);        // Add force to the ball
    }

    //external collision, add force
    public void AddForce(Vector2 force)
    {
        _rigidBody.AddForce(force);
    }

    //reset our values for ball
    public void ResetPosition()
    {
        _rigidBody.position = Vector3.zero;
        _rigidBody.velocity = Vector3.zero;

        AddStartingForce();
    }

}
