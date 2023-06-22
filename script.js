document.addEventListener("DOMContentLoaded", () => {
    const getQuizDetailsButton = document.getElementById("get-details-btn");
    const quizIdInput = document.getElementById("quiz-id");
    const titleElement = document.getElementById("title");
    const descriptionElement = document.getElementById("description");
    const questionInput = document.getElementById("question-input");
    const getAnswerButton = document.getElementById("get-answer-btn");
    const questionDropdown = document.getElementById("question-dropdown");
    const answerSection = document.getElementById("answer-section");
    const answerElement = document.getElementById("answer");
    const sessionDropdown = document.getElementById("session-dropdown");
    const refreshIcon = document.getElementById("refresh-icon");
    const historyIcon = document.getElementById("history-icon");
    
    
    function removeOptions(selectElement) {
      var i, L = selectElement.options.length - 1;
      for(i = L; i >= 0; i--) {
          selectElement.remove(i);
      }
    }
    // Event listener for the "Get Game Details" button
    getQuizDetailsButton.addEventListener("click", () => {
      const quizId = quizIdInput.value;
      // Perform API request to get game details based on quizId
      // Update titleElement and descriptionElement with the retrieved data
      // Populate questionDropdown with available questions
      // Handle error cases appropriately
      
        // set the data varible to a fetch request to the api with the quizId and no-cors

        const proxyUrl = 'https://mysterious-brushlands-13683-0083c994a678.herokuapp.com/';
        const targetUrl = 'https://play.kahoot.it/rest/kahoots/';

        function getQuizDetails(quizId) {
        const apiUrl = proxyUrl + targetUrl + quizId;

        let response = fetch(apiUrl)
            .then(response => response.json())
            .then(data => {
                // Check if the response returns anthing else than 200
                if (data.visibility !== 1) {
                    titleElement.innerHTML = "Quiz is private or does not exist. If you think this is an error, please contact the developer."
                    // Clear tzhe question dropdown
                    removeOptions(questionDropdown);
                    return;
                }
                titleElement.innerHTML = data.title;
                descriptionElement.innerHTML = data.description;
                localStorage.setItem("quizID", quizId)
                // Populate questionDropdown with available questions
                for (let i = 0; i < data.questions.length; i++) {
                    const question = data.questions[i];
                    const option = document.createElement("option");
                    option.text = question.question;
                    option.value = question.question;
                    questionDropdown.add(option);
                }

                
                
            })
            .catch(error => {
            // Handle any errors that occur during the fetch request
            console.error('Error:', error);
            });
            
        }

        const data = getQuizDetails(quizId);

        

    });
  
    // Event listener for the "Get Answer" button
    getAnswerButton.addEventListener("click", () => {
      const question = questionInput.value;
      const proxyUrl = 'https://mysterious-brushlands-13683-0083c994a678.herokuapp.com/';
      const targetUrl = 'https://play.kahoot.it/rest/kahoots/';
      quizId = localStorage.getItem("quizID")
    
      function getAnswer(quizId) {
        const apiUrl = proxyUrl + targetUrl + quizId;
    
        let response = fetch(apiUrl)
          .then(response => response.json())
          .then(data => {
            // Go through the questions array and find the question that matches the questionInput
            const questionData = data.questions.find(q => q.question === question);
    
            // If the question is found, update the answerElement with the correct answer by going through the choices array and looking for the choice with the value of true
            if (questionData) {
              // Set correctAnswer to the choice with the value of true, if there are multiple correct answers, correctAnswer will be an array, otherwise it will be an object
              const correctAnswer = questionData.choices.filter(c => c.correct);
    
              // Check if there are multiple correct answers
              if (correctAnswer && correctAnswer.length > 1) {
                // If there are multiple correct answers, update the answerElement with all of the correct answers separated by a comma
                answerElement.innerHTML = correctAnswer.map(c => c.answer).join(", ");
              } else if (correctAnswer && correctAnswer.length === 1) {
                // If there is only one correct answer, update the answerElement with the correct answer
                answerElement.innerHTML = correctAnswer[0].answer;
              } else {
                // If there is no correct answer, display a message indicating that no correct answer was found
                answerElement.innerHTML = "No correct answer found.";
              }
    
              // Set the div with the ID answer-section to display
              answerSection.style.display = "block";
            } else {
              // If the question is not found, display a message indicating that the question was not found
              answerElement.innerHTML = "Question not found.";
            }
          })
      }
    
      const answer = getAnswer(quizId);
    });
  
    // Event listener for question dropdown selection change
    questionDropdown.addEventListener("change", () => {
      const selectedQuestion = questionDropdown.value;
      // Perform API request to get answer based on selectedQuestion
      // Update answerElement with the retrieved data
      // Handle error cases appropriately

      const proxyUrl = 'https://mysterious-brushlands-13683-0083c994a678.herokuapp.com/';
      const targetUrl = 'https://play.kahoot.it/rest/kahoots/';
      quizId = localStorage.getItem("quizID")
      function getAnswer(quizId) {
        const apiUrl = proxyUrl + targetUrl + quizId;
      
        let response = fetch(apiUrl)
          .then(response => response.json())
          .then(data => {
            // Go through the questions array and find the question that matches the questionInput
            const question = data.questions.find(q => q.question === selectedQuestion);
      
            // If the question is found, update the answerElement with the correct answer by going through the choices array and looking for the choice with the value of true
            if (question) {
              const correctAnswer = question.choices.filter(c => c.correct);
    
              // Check if there are multiple correct answers
              if (correctAnswer && correctAnswer.length > 1) {
                // If there are multiple correct answers, update the answerElement with all of the correct answers separated by a comma
                answerElement.innerHTML = correctAnswer.map(c => c.answer).join(", ");
              } else if (correctAnswer && correctAnswer.length === 1) {
                // If there is only one correct answer, update the answerElement with the correct answer
                answerElement.innerHTML = correctAnswer[0].answer;
              } else {
                // If there is no correct answer, display a message indicating that no correct answer was found
                answerElement.innerHTML = "No correct answer found.";
              }
    
              // Set the div with the ID answer-section to display
              answerSection.style.display = "block";
            }
          })
      }

      const answer = getAnswer(quizId);

    });
  
  });