using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{

    private int _playerScore;
    private int _computerScore;

    public Ball ball;
    public Text playerScoreText;
    public Text computerScoreText;

    public void PlayerScores()
    {
        _playerScore += 1;
        this.ball.ResetPosition();
        this.playerScoreText.text = _playerScore.ToString();
    }

    public void ComputerScores()
    {
        _computerScore += 1;
        this.ball.ResetPosition();
        this.computerScoreText.text = _computerScore.ToString();

    }
       
}
