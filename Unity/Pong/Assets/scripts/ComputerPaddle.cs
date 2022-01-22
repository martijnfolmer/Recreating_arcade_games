using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class ComputerPaddle : Paddle
{

    public Rigidbody2D ball;        // Find the rigidbody of the ball



    private void FixedUpdate()
    {

        if (this.ball.velocity.x > 0.0f) // velocity is bigger than 0, so it is moving towards us
        {
            if (this.ball.position.y > this.transform.position.y) // ball is above us
            {
                _rigidbody.AddForce(Vector2.up * this.speed);
            }
            else if (this.ball.position.y < this.transform.position.y)
            {
                _rigidbody.AddForce(Vector2.down * this.speed);
            }
        }
        else // ball is moving away from us, so we can return back to center position
        {
            if (this.transform.position.y > 0.0f) 
            {
                _rigidbody.AddForce(Vector2.down * this.speed);
            }
            else if (this.transform.position.y < 0.0f)
            {
                _rigidbody.AddForce(Vector2.up * this.speed);
            }
        }

    }

}
