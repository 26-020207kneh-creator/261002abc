import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="벽돌깨기 게임",
    page_icon="🎮",
    layout="centered"
)

st.title("🎮 벽돌깨기 게임")
st.write("← → 키로 패들을 움직이세요!")

game = """
<!DOCTYPE html>
<html>
<head>
<style>
    body {
        margin: 0;
        background: #111827;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: Arial, sans-serif;
    }

    canvas {
        border: 3px solid #38bdf8;
        background: #020617;
        box-shadow: 0 0 25px #0ea5e9;
    }
</style>
</head>

<body>

<canvas id="gameCanvas" width="480" height="600"></canvas>

<script>

const canvas = document.getElementById("gameCanvas");
const ctx = canvas.getContext("2d");

let ballRadius = 8;

let x = canvas.width / 2;
let y = canvas.height - 60;

let dx = 3;
let dy = -3;

let paddleHeight = 12;
let paddleWidth = 90;

let paddleX = (canvas.width - paddleWidth) / 2;

let rightPressed = false;
let leftPressed = false;

let score = 0;
let lives = 3;

let gameRunning = true;


// 벽돌 설정
const brickRowCount = 6;
const brickColumnCount = 7;

const brickWidth = 55;
const brickHeight = 20;

const brickPadding = 10;

const brickOffsetTop = 45;
const brickOffsetLeft = 20;

let bricks = [];

for (let c = 0; c < brickColumnCount; c++) {
    bricks[c] = [];

    for (let r = 0; r < brickRowCount; r++) {
        bricks[c][r] = {
            x: 0,
            y: 0,
            status: 1
        };
    }
}


// 키보드
document.addEventListener("keydown", keyDownHandler);
document.addEventListener("keyup", keyUpHandler);

function keyDownHandler(e) {

    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = true;
    }

    else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = true;
    }
}

function keyUpHandler(e) {

    if (e.key === "Right" || e.key === "ArrowRight") {
        rightPressed = false;
    }

    else if (e.key === "Left" || e.key === "ArrowLeft") {
        leftPressed = false;
    }
}


// 공
function drawBall() {

    ctx.beginPath();

    ctx.arc(
        x,
        y,
        ballRadius,
        0,
        Math.PI * 2
    );

    ctx.fillStyle = "#facc15";
    ctx.fill();

    ctx.closePath();
}


// 패들
function drawPaddle() {

    ctx.beginPath();

    ctx.roundRect(
        paddleX,
        canvas.height - paddleHeight - 10,
        paddleWidth,
        paddleHeight,
        6
    );

    ctx.fillStyle = "#38bdf8";
    ctx.fill();

    ctx.closePath();
}


// 벽돌
function drawBricks() {

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            if (bricks[c][r].status === 1) {

                let brickX =
                    c * (brickWidth + brickPadding)
                    + brickOffsetLeft;

                let brickY =
                    r * (brickHeight + brickPadding)
                    + brickOffsetTop;

                bricks[c][r].x = brickX;
                bricks[c][r].y = brickY;

                ctx.beginPath();

                ctx.roundRect(
                    brickX,
                    brickY,
                    brickWidth,
                    brickHeight,
                    4
                );

                const colors = [
                    "#ef4444",
                    "#f97316",
                    "#eab308",
                    "#22c55e",
                    "#06b6d4",
                    "#8b5cf6"
                ];

                ctx.fillStyle = colors[r];

                ctx.fill();

                ctx.closePath();
            }
        }
    }
}


// 점수
function drawScore() {

    ctx.font = "18px Arial";
    ctx.fillStyle = "#ffffff";

    ctx.fillText(
        "점수: " + score,
        15,
        25
    );
}


// 목숨
function drawLives() {

    ctx.font = "18px Arial";
    ctx.fillStyle = "#ffffff";

    ctx.fillText(
        "목숨: " + lives,
        canvas.width - 75,
        25
    );
}


// 충돌 검사
function collisionDetection() {

    for (let c = 0; c < brickColumnCount; c++) {

        for (let r = 0; r < brickRowCount; r++) {

            let b = bricks[c][r];

            if (b.status === 1) {

                if (
                    x > b.x &&
                    x < b.x + brickWidth &&
                    y > b.y &&
                    y < b.y + brickHeight
                ) {

                    dy = -dy;

                    b.status = 0;

                    score += 10;

                    // 모든 벽돌 제거 확인
                    if (score === brickRowCount * brickColumnCount * 10) {
                        gameRunning = false;

                        setTimeout(function() {
                            alert("🎉 게임 클리어!");
                            location.reload();
                        }, 100);
                    }
                }
            }
        }
    }
}


// 게임 업데이트
function update() {

    if (!gameRunning) {
        return;
    }

    collisionDetection();

    // 벽 충돌
    if (
        x + dx > canvas.width - ballRadius ||
        x + dx < ballRadius
    ) {
        dx = -dx;
    }

    // 천장 충돌
    if (y + dy < ballRadius) {

        dy = -dy;

    }

    // 패들과 충돌
    else if (
        y + dy >
        canvas.height - paddleHeight - 10 - ballRadius
    ) {

        if (
            x > paddleX &&
            x < paddleX + paddleWidth
        ) {

            // 패들의 어느 위치에 맞았는지에 따라 방향 변경
            let hitPosition =
                (x - (paddleX + paddleWidth / 2))
                / (paddleWidth / 2);

            dx = hitPosition * 5;

            dy = -Math.abs(dy);

        }

        else if (
            y + dy >
            canvas.height - ballRadius
        ) {

            lives--;

            if (lives <= 0) {

                gameRunning = false;

                setTimeout(function() {
                    alert("💥 게임 오버!");
                    location.reload();
                }, 100);

            }

            else {

                x = canvas.width / 2;
                y = canvas.height - 60;

                dx = 3;
                dy = -3;

                paddleX =
                    (canvas.width - paddleWidth) / 2;
            }
        }
    }

    x += dx;
    y += dy;


    // 패들 이동
    if (rightPressed) {

        paddleX += 7;

        if (
            paddleX + paddleWidth >
            canvas.width
        ) {
            paddleX =
                canvas.width - paddleWidth;
        }
    }

    else if (leftPressed) {

        paddleX -= 7;

        if (paddleX < 0) {
            paddleX = 0;
        }
    }
}


// 화면 그리기
function draw() {

    ctx.clearRect(
        0,
        0,
        canvas.width,
        canvas.height
    );

    drawBricks();

    drawBall();

    drawPaddle();

    drawScore();

    drawLives();

    update();

    requestAnimationFrame(draw);
}

draw();

</script>

</body>
</html>
"""

components.html(game, height=630, scrolling=False)
