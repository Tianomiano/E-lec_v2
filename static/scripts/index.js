const editQuestionOptions = document.querySelectorAll(".edit-question-option");
const deleteQuestionOptions = document.querySelectorAll(".delete-question-option");

editQuestionOptions.forEach(editQuestionOption => {
    editQuestionOption.style.display = "none";
});

deleteQuestionOptions.forEach(deleteQuestionOption => {
    deleteQuestionOption.style.display = "none";
});
let currentUserId; 
async function fetchUserId() {
    try {
        const response = await fetch("/api/v1/getuser", {
            method: "GET",
            headers: {
                "Authorization": getSessionToken()
            }
        });
        
        if (response.ok) {
            const userData = await response.json();
            currentUserId = userData.user_id;
        } else {
            console.error("Error fetching user details:", response.statusText);
        }
    } catch (error) {
        console.error("Error fetching user details:", error);
    }
}

fetchUserId();

// Get the questions container
const questionsSection = document.getElementById("questions-section");
const repliesSection = document.getElementById("replies-section");

// Get the view replies button and question-replies container
const viewRepliesButton = document.getElementById("view-replies-button");
const questionRepliesContainer = document.getElementById("question-replies-container");

// Initial subject (Architecture)
let currentSubject = "Architecture";

// Function to fetch and display questions
function fetchAndDisplayQuestions(subject) {
    fetch(`/api/v1/questions?subject=${subject}`)
        .then(response => response.json())
        .then(data => {
            // Clear previous questions
            questionsSection.innerHTML = "";

            // Create a new question element for each question
            data.questions.forEach(question => {
                const questionElement = document.createElement("div");
                questionElement.className = "question";
                questionElement.setAttribute("data-question-id", question.question_id);
                questionElement.setAttribute("data-author-id", question.author_id);
                questionElement.innerHTML = `
                    <h2>${question.subject}</h2>
                    <p class="que">${question.question}</p>
                    <p class="posted">Posted on: ${question.date_posted}</p>
                    <button class="view-replies-btn" data-question-id="${question.question_id}">View Replies</button>
                    <button class="edit-question-option" data-question-id="${question.question_id}" data-question-content="${question.question}">Edit</button>
                    <button class="delete-question-option" data-question-id="${question.question_id}">Delete</button>
                `;
                const editQuestionOption = questionElement.querySelector(".edit-question-option");
                const deleteQuestionOption = questionElement.querySelector(".delete-question-option");
                if (currentUserId) {
                    if (currentUserId === question.author_id) {
                        editQuestionOption.style.display = "inline";
                        deleteQuestionOption.style.display = "inline";
                    } else {
                        editQuestionOption.style.display = "none";
                        deleteQuestionOption.style.display = "none";
                    }
                } else {
                    editQuestionOption.style.display = "none";
                    deleteQuestionOption.style.display = "none";
                }
                questionElement.querySelector(".edit-question-option").addEventListener("click", (event) => {
                    const questionId = event.target.getAttribute("data-question-id");
                    const questionContent = event.target.getAttribute("data-question-content");
                    
                    // Prompt user to edit the question
                    const updatedQuestionContent = prompt("Edit the question:", questionContent);
                    if (updatedQuestionContent !== null) {
                        const token = getSessionToken();
                        const headers = {
                            "Authorization": token,
                            "Content-Type": "application/json"
                        };
            
                        const data = {
                            content: updatedQuestionContent
                        };
            
                        fetch(`/api/v1/questions/${questionId}`, {
                            method: "PUT",
                            headers: headers,
                            body: JSON.stringify(data)
                        })
                        .then(response => response.json())
                        .then(result => {
                            console.log(result.message);
                            fetchAndDisplayQuestions(subject);
                        })
                        .catch(error => {
                            console.error("Error editing question:", error);
                        });
                    }
                });
                questionElement.querySelector(".delete-question-option").addEventListener("click", async (event) => {
                    event.stopPropagation();
                    const questionId = event.target.getAttribute("data-question-id");
            
                    if (confirm("Are you sure you want to delete this question?")) {
                        const token = getSessionToken();
                        const headers = {
                            "Authorization": token
                        };
            
                        try {
                            const response = await fetch(`/api/v1/questions/del/${questionId}`, {
                                method: "DELETE",
                                headers: headers
                            });
            
                            if (response.ok) {
                                fetchAndDisplayQuestions(subject);
                            } else {
                                console.error("Error deleting question:", response.status);
                            }
                        } catch (error) {
                            console.error("Error deleting question:", error);
                        }
                    }
                });
                    
                questionsSection.appendChild(questionElement);

                questionsSection.addEventListener("click", (event) => {
                    const target = event.target;
                
                    // Check if the clicked element is a "View Replies" button
                    if (target.classList.contains("view-replies-btn")) {
                        const questionElement = target.closest(".question");
                        const questionId = questionElement.getAttribute("data-question-id");
                
                        // Update the selected question and its replies
                        document.getElementById("selected-question-subject").textContent = questionElement.querySelector("h2").textContent;
                        document.getElementById("selected-question-content").textContent = questionElement.querySelector("p").textContent;
                
                        // Fetch and display replies for the selected question
                        fetchAndDisplayReplies(questionId);
                    }
                });
                // Create reply input and button elements
                const replyInputContainer = document.createElement("div");
                replyInputContainer.className = "reply-input-container";
                replyInputContainer.innerHTML = `
                    <textarea class="reply-input" placeholder="Write a reply..." rows="2"></textarea>
                    <button class="send-reply-button">&#10148;</button>
                `;

                const sendReplyButton = replyInputContainer.querySelector(".send-reply-button");
                if (currentUserId) {
                    replyInputContainer.style.display = "block";
                } else {
                    replyInputContainer.style.display = "none";
                }
                
                sendReplyButton.addEventListener("click", () => {
                    const replyInput = replyInputContainer.querySelector(".reply-input");
                    const content = replyInput.value.trim();
                    if (content) {
                        const questionId = questionElement.getAttribute("data-question-id");
                        sendReply(questionId, content);
                        replyInput.value = ""; // Clear the input field
                    } else {
                        console.error("No reply content entered");
                    }
                });

                // Insert reply input and button after the question
                questionElement.appendChild(replyInputContainer);
            });
        })
        .catch(error => {
            console.error("Error fetching questions:", error);
        });
}

// Function to fetch and display replies
function fetchAndDisplayReplies(questionId) {
    // Fetch replies for the specified question
    fetch(`/api/v1/questions/${questionId}`)
        .then(response => response.json())
        .then(data => {
            const repliesSectionContainer = document.getElementById("replies-section-container");
            const selectedQuestionSubject = document.getElementById("selected-question-subject");
            const selectedQuestionContent = document.getElementById("selected-question-content");
            const repliesSection = document.getElementById("replies-section");

            // Update the selected question and its replies
            selectedQuestionSubject.textContent = data.subject;
            selectedQuestionContent.textContent = data.question;

            // Clear previous replies
            repliesSection.innerHTML = "";

            // Create a new reply element for each reply
            data.replies.forEach(reply => {
                const replyElement = document.createElement("div");
                replyElement.className = "reply";
                replyElement.innerHTML = `
                    <div class="reply-content">
                        <p>${reply.content}</p>
                        <div class="date_p">
                            <p>Posted on: ${reply.date_posted}</p>
                        </div>
                        <div class="reply-options">
                            <span class="options-icon">&#8230;</span>
                            <div class="options-menu">
                                <span class="edit-option" data-reply-id="${reply.reply_id}">Edit</span>
                                <span class="delete-option" data-reply-id="${reply.reply_id}">Delete</span>
                            </div>
                        </div>
                    </div>
                `;
                const editReplyOption = replyElement.querySelector(".edit-option");
                const deleteReplyOption = replyElement.querySelector(".delete-option");
                if (currentUserId) {
                    if (currentUserId === reply.author_id) {
                        editReplyOption.style.display = "inline";
                        deleteReplyOption.style.display = "inline";
                    } else {
                        editReplyOption.style.display = "none";
                        deleteReplyOption.style.display = "none";
                    }
                } else {
                    editReplyOption.style.display = "none";
                    deleteReplyOption.style.display = "none";
                }
                repliesSection.appendChild(replyElement);

                const optionsMenu = replyElement.querySelector(".options-menu");
                const optionsIcon = replyElement.querySelector(".options-icon");

                optionsIcon.addEventListener("click", (event) => {
                    event.stopPropagation();
                    optionsMenu.classList.toggle("show");
                });

                const deleteOption = replyElement.querySelector(".delete-option");

                replyElement.querySelector(".edit-option").addEventListener("click", (event) => {
                    const replyId = event.target.getAttribute("data-reply-id");
                    const replyContent = event.target.getAttribute("data-reply-content");
                    const editButton = event.target;

                    const inlineEditBox = document.createElement("div");
                    inlineEditBox.className = "inline-edit-box";

                    const editTextarea = document.createElement("textarea");
                    editTextarea.value = replyContent;
                    inlineEditBox.appendChild(editTextarea);

                    const saveButton = document.createElement("button");
                    saveButton.textContent = "Save";
                    saveButton.addEventListener("click", async () => {
                        const updatedContent = editTextarea.value.trim();
                        if (updatedContent) {
                            const token = getSessionToken();
                            const headers = {
                                "Authorization": token,
                                "Content-Type": "application/json"
                            };

                            const data = {
                                content: updatedContent
                            };

                            try {
                                const response = await fetch(`/api/v1/replies/${replyId}`, {
                                    method: "PUT",
                                    headers: headers,
                                    body: JSON.stringify(data)
                                });

                                if (response.ok) {
                                    // Refresh the replies after editing
                                    fetchAndDisplayReplies(questionId);
                                } else {
                                    console.error("Error editing reply:", response.status);
                                }
                            } catch (error) {
                                console.error("Error editing reply:", error);
                            }
                        }
                    });
                    inlineEditBox.appendChild(saveButton);

                    // Replace the "Edit" button with the inline edit box
                    editButton.parentNode.insertBefore(inlineEditBox, editButton);
                    editButton.style.display = "none";
                });


                deleteOption.addEventListener("click", async (event) => {
                    event.stopPropagation();
                    const replyId = event.target.getAttribute("data-reply-id");
                
                    if (confirm("Are you sure you want to delete this reply?")) {
                        const token = getSessionToken();
                        const headers = {
                            "Authorization": token
                        };
                
                        try {
                            const response = await fetch(`/api/v1/replies/del/${replyId}`, {
                                method: "DELETE",
                                headers: headers
                            });
                
                            if (response.ok) {
                                // Refresh the replies after deleting
                                fetchAndDisplayReplies(questionId);
                            } else {
                                console.error("Error deleting reply:", response.status);
                            }
                        } catch (error) {
                            console.error("Error deleting reply:", error);
                        }
                    }
                });                
            });

            // Show the replies section container
            repliesSectionContainer.classList.add("show");
        })
        .catch(error => {
            console.error("Error fetching replies:", error);
        });
}

// Function to send a new reply using AJAX
function sendReply(questionId, content) {
    const token = getSessionToken();

    if (!token) {
        console.log("Authorization token missing");
        return;
    }

    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

    const data = {
        content: content
    };

    // Send the new reply using AJAX
    $.ajax({
        type: "POST",
        url: `/api/v1/questions/${questionId}/reply`,
        headers: headers,
        data: JSON.stringify(data),
        success: function(response) {
            console.log("Reply posted successfully");
            fetchAndDisplayReplies(questionId); // Refresh replies after posting
        },
        error: function(error) {
            console.error("Error posting reply:", error);
        }
    });
}

// Add event listener to the close icon
const closeIcon = document.getElementById("close-icon");
closeIcon.addEventListener("click", () => {
    // Hide the replies section container and show the questions section
    const repliesSectionContainer = document.getElementById("replies-section-container");
    repliesSectionContainer.classList.remove("show");
});
document.getElementById("write-question-button").addEventListener("click", () => {
    const writeButton = document.getElementById("write-question-button");
    const writeForm = document.getElementById("write-question-form");

    // Get the button's position
    const buttonRect = writeButton.getBoundingClientRect();
    const buttonTop = buttonRect.top + window.scrollY;
    const buttonLeft = buttonRect.left + window.scrollX;

    // Set the form's position
    writeForm.style.top = buttonTop + "px";
    writeForm.style.left = buttonLeft + "px";

    // Show the form
    writeForm.classList.toggle("hidden");
});

// Post question button
document.getElementById("post-question-button").addEventListener("click", async () => {
    const subject = document.getElementById("question-subject").value;
    const content = document.getElementById("question-content").value;

    if (!content.trim()) {
        alert("Question content cannot be empty");
        return; // Exit the function if content is empty
    }
    
    const token = getSessionToken();
    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

    const data = {
        subject: subject,
        content: content
    };

    try {
        const response = await fetch("/api/v1/questions", {
            method: "POST",
            headers: headers,
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Question posted successfully");
            // Clear and hide the form
            document.getElementById("question-subject").value = "Architecture"; // Reset the subject
            document.getElementById("question-content").value = ""; // Clear the content
            document.getElementById("write-question-form").classList.add("hidden");
            fetchAndDisplayQuestions(subject);
        } else {
            const errorData = await response.json();
            alert("Error posting question: " + errorData.error);
        }
    } catch (error) {
        console.error("Error posting question:", error);
    }
});


// Fetch and display initial questions (Architecture)
fetchAndDisplayQuestions(currentSubject);

// Handle subject clicks
const subjectLinks = document.querySelectorAll(".subul a");
subjectLinks.forEach(link => {
    link.addEventListener("click", event => {
        event.preventDefault();
        const subject = link.textContent.trim();

        fetchAndDisplayQuestions(subject);
    });
});
