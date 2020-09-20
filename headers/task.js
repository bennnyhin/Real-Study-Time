window.onload = () => {
    let timeElapsed = 0;
    let timer = null;

    let incrementTime = () => {
        timeElapsed++;
    }

    let startTimer = () => {
        timer = setInterval(incrementTime, 1000);
    }

    let pauseTimer = () => {
        clearInterval(timer);
        timer = null;
    }
}