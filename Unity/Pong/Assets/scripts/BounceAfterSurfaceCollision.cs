using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BounceAfterSurfaceCollision : MonoBehaviour
{

    public float bounceStrength;

    private void OnCollisionEnter2D(Collision2D collision)
    {
        Ball ball = collision.gameObject.GetComponent<Ball>();      //get the ball part of this collision
        if (ball != null)
        {
            Vector2 normal = collision.GetContact(0).normal;    // get the contact point of the collision
            ball.AddForce(-normal * this.bounceStrength);        // add force to the ball which is connected
        }
    }
}
