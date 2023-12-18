// generate the current logged in user id
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

// Show or hide the write button based on whether the user is logged in
const writeButton = document.getElementById("write-button");


// Write button
document.getElementById("write-button").addEventListener("click", () => {
    const writeForm = document.getElementById("write-article-form");
    writeForm.classList.toggle("hidden");
});

// Post question button
document.getElementById("post-article-button").addEventListener("click", async () => {
    const title = document.getElementById("article-title").value;
    const content = document.getElementById("article-content").value;

    if (!content.trim()) {
        alert("Question content cannot be empty");
        return; // Exit the function if content is empty
    }
    if (!title.trim()) {
        alert("Title cannot be empty");
        return; // Exit the function if content is empty
    }

    
    const token = getSessionToken();
    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

    const data = {
        title: title,
        content: content
    };

    try {
        const response = await fetch("/api/v1/articles", {
            method: "POST",
            headers: headers,
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Article posted successfully");
            document.getElementById("article-title").value = "";
            document.getElementById("article-content").value = "";
            document.getElementById("write-article-form").classList.add("hidden");
        } else {
            const errorData = await response.json();
            alert("Error posting article: " + errorData.error);
        }
    } catch (error) {
        console.error("Error article:", error);
    }
});
function toggleWriteButton(loggedIn) {
    const writeButton = document.getElementById("write-button");
    if (loggedIn) {
        writeButton.style.display = "block";
    } else {
        writeButton.style.display = "none";
    }
}
// Function to truncate a string to a specified number of words
function truncateWords(str, numWords) {
    const words = str.split(' ');
    if (words.length > numWords) {
        return words.slice(0, numWords).join(' ') + '...';
    } else {
        return str;
    }
}
// Function to show the modal with full article content
function openModal(title, content, date, id) {
    const modal = document.getElementById("articleModal");
    const modalContent = document.getElementById("fullArticleContent");

    modalContent.innerHTML = "";

    
    const article_id = id;

    const titleElement = document.createElement("h2");
    titleElement.textContent = title;

    const dateElement = document.createElement("h3");
    dateElement.textContent = "Date Posted: " + date;

    modalContent.appendChild(titleElement);

    const contentElement = document.createElement("p");
    contentElement.textContent = content;

    modalContent.appendChild(contentElement);
    modalContent.appendChild(dateElement);

    const editButton = document.createElement("button");
    editButton.textContent = "Edit";
    editButton.classList.add("edit-button");
    editButton.addEventListener("click", function() {
        // Enable editing of title and content
        titleElement.contentEditable = true;
        contentElement.contentEditable = true;
        submitButton.style.display = "block";
        editButton.style.display = "none";
    });

    const submitButton = document.createElement("button");
    submitButton.textContent = "Submit";
    submitButton.style.display = "none";
    submitButton.classList.add("submit-button");
    submitButton.addEventListener("click", async function() {
        // Send a PUT request to update the article
        const updatedTitle = titleElement.textContent;
        const updatedContent = contentElement.textContent;

        try {
            const response = await fetch(`/api/v1/articles/${article_id}`, {
                method: "PUT",
                headers: {
                    "Authorization": getSessionToken(),
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ title: updatedTitle, content: updatedContent }),
            });

            if (response.ok) {
                // Article updated successfully
                // Disable editing
                titleElement.contentEditable = false;
                contentElement.contentEditable = false;
                submitButton.style.display = "none";
                editButton.style.display = "block";
                alert("Article updated successfully");
            } else {
                // Handle the case where the update request fails
                console.error("Error updating article:", response.status);
                alert("Error updating article");
            }
        } catch (error) {
            // Handle any network or other errors here
            console.error("Error updating article:", error);
            alert("Error updating article");
        }
    });

    
    modalContent.appendChild(titleElement);
    modalContent.appendChild(dateElement);
    modalContent.appendChild(contentElement);
    modalContent.appendChild(editButton);
    modalContent.appendChild(submitButton);


    // Show the modal
    modal.style.display = "block";

    // Close the modal when the close button is clicked
    const closeModal = document.getElementById("closeModal");
    closeModal.onclick = function() {
        modal.style.display = "none";
    };
}

// Function to create and append an article element
function createArticleElement(article) {
    const articleDiv = document.createElement("div");
    articleDiv.classList.add("article");
    articleDiv.classList.add("article-border"); 

    const titleElement = document.createElement("h2");
    titleElement.textContent = article.title;
    articleDiv.appendChild(titleElement);

    const contentElement = document.createElement("p");
    const truncatedContent = truncateWords(article.content, 100);
    contentElement.textContent = truncatedContent;
    articleDiv.appendChild(contentElement);

    const dateElement = document.createElement("h3");
    dateElement.textContent = "Date Posted: " + article.date_posted;
    articleDiv.appendChild(dateElement);

    const readMoreButton = document.createElement("button");
    readMoreButton.textContent = "Read More";
    readMoreButton.classList.add("read-more-button");
    readMoreButton.addEventListener("click", function() {
        openModal(article.title, article.content, article.date_posted, article.article_id);
    });

    articleDiv.appendChild(readMoreButton);

    if (currentUserId === article.author_id) {
        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.classList.add("delete-button");
        deleteButton.addEventListener("click", async function() {
            try {
                const response = await fetch(`/api/v1/articles/${article.article_id}`, {
                    method: "DELETE",
                    headers: {
                        "Authorization": getSessionToken(),
                    },
                });

                if (response.ok) {
                    articleDiv.remove();
                    alert("Article deleted successfully");
                } else {
                    console.error("Error deleting article:", response.status);
                }
            } catch (error) {
                console.error("Error deleting article:", error);
            }
        });

        articleDiv.appendChild(deleteButton);
    }

    return articleDiv;
}

// Function to fetch and display articles
async function fetchAndDisplayArticles() {
    try {
        const response = await fetch("/api/v1/articles", {
            method: "GET",
        });

        if (response.ok) {
            const articlesData = await response.json();
            const articles = articlesData.articles;

            const articlesSection = document.getElementById("articles-section");
            articlesSection.innerHTML = ""; 

            articles.forEach((article) => {
                const articleElement = createArticleElement(article);
                articlesSection.appendChild(articleElement);
            });
        } else {
            console.error("Error fetching articles:", response.status);
        }
    } catch (error) {
        console.error("Error fetching articles:", error);
    }
}

// Call the fetchAndDisplayArticles function to populate the articles section
fetchAndDisplayArticles();
setInterval(fetchAndDisplayArticles, 30000)
