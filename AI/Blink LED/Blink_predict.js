    // run the webcam image through the image model
    async function predict() {
        // predict can take in an image, video or canvas html element
        const prediction = await model.predict(webcam.canvas);
        for (let i = 0; i < maxPredictions; i++) {
            const classPrediction =
                prediction[i].className + ": " + prediction[i].probability.toFixed(2);
            labelContainer.childNodes[i].innerHTML = classPrediction;
        }

        let highest = prediction.reduce((prev, current) =>
        prev.probability > current.probability ? prev : current
      );
        

        if (highest.probability > 0.85) {
        console.log("Prediction:", highest.className);

        if (highest.className === "Mobile") {
          sendToArduino("L");
        console.log("L:", highest.className);
        } else if (highest.className === "Wheel") {
          sendToArduino("R");
        console.log("R:", highest.className);

        }
      }

    }
