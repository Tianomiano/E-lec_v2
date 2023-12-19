// Function to load videos based on the selected subject
function loadVideos(subject) {
    $.ajax({
        url: `api/v1/videos/${subject}`,
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            // Update the content of the vid-middle div with the new videos
            updateVideoList(data.videos);
        },
        error: function (error) {
            console.error('Error loading videos:', error);
        }
    });
}

function updateVideoList(videos) {
    const vidMiddleDiv = $('.vid-middle');
    vidMiddleDiv.empty(); // Clear existing content

    // Create a container div for flex layout
    const flexContainer = $('<div class="video-container"></div>');

    // Iterate through the videos and append them to the flex container
    videos.forEach(function (video) {
        const datePosted = moment(video.date_posted).utc(); // Convert to moment object
        const currentDate = moment().utc(); // Current date

        // Calculate the difference in time
        const diffInSeconds = Math.abs(currentDate.diff(datePosted, 'seconds'));
        const diffInMinutes = Math.abs(currentDate.diff(datePosted, 'minutes'));
        const diffInHours = Math.abs(currentDate.diff(datePosted, 'hours'));
        const diffInDays = Math.abs(currentDate.diff(datePosted, 'days'));
        const diffInWeeks = Math.abs(currentDate.diff(datePosted, 'weeks'));
        const diffInMonths = Math.abs(currentDate.diff(datePosted, 'months'));
        const diffInYears = Math.abs(currentDate.diff(datePosted, 'years'));

        // Determine the appropriate time unit to display
        let timeDisplay;
        if (diffInSeconds < 60) {
            timeDisplay = `Posted: ${Math.round(diffInSeconds)} second${diffInSeconds !== 1 ? 's' : ''} ago`;
        } else if (diffInMinutes < 60) {
            timeDisplay = `Posted: ${Math.round(diffInMinutes)} minute${diffInMinutes !== 1 ? 's' : ''} ago`;
        } else if (diffInHours < 24) {
            timeDisplay = `Posted: ${Math.round(diffInHours)} hour${diffInHours !== 1 ? 's' : ''} ago`;
        } else if (diffInDays < 7) {
            timeDisplay = `Posted: ${Math.round(diffInDays)} day${diffInDays !== 1 ? 's' : ''} ago`;
        } else if (diffInWeeks < 4.35) {
            timeDisplay = `Posted: ${Math.round(diffInWeeks)} week${diffInWeeks !== 1 ? 's' : ''} ago`;
        } else if (diffInMonths < 12) {
            timeDisplay = `Posted: ${Math.round(diffInMonths)} month${diffInMonths !== 1 ? 's' : ''} ago`;
        } else {
            timeDisplay = `Posted: ${Math.round(diffInYears)} year${diffInYears !== 1 ? 's' : ''} ago`;
        }

        const videoElement = `
            <div class="video-item">
                <p>${video.embed_code}</p>
                <h3>${video.title}</h3>
                <p>${timeDisplay}</p>
            </div>`;
        flexContainer.append(videoElement);
    });

    // Append the flex container to the vid-middle div
    vidMiddleDiv.append(flexContainer);
}
    

// Default: Load videos for the 'Architecture' subject on page load
loadVideos('Architecture');

// Event listener for subject links
$('.subul a').on('click', function (event) {
    event.preventDefault();
    const selectedSubject = $(this).text().trim();
    loadVideos(selectedSubject);
});



document.getElementById("post-video").addEventListener("click", () => {
    const postButton = document.getElementById("post-video");
    const postForm = document.getElementById("post-video-form");

    // Get the button's position
    const buttonRect = postButton.getBoundingClientRect();
    const buttonTop = buttonRect.top + window.scrollY;
    const buttonLeft = buttonRect.left + window.scrollX;

    // Set the form's position
    postForm.style.top = buttonTop + "px";
    postForm.style.left = buttonLeft + "px";

    // Show the form
    postForm.classList.toggle("hidden");
});
// Post question button
document.getElementById("post-video-button").addEventListener("click", async () => {
    const subject = document.getElementById("video-subject").value;
    const title = document.getElementById("video-title").value;
    const videoUrl = document.getElementById("video-url").value;


    if (!title.trim()) {
        alert("title content cannot be empty");
        return; // Exit the function if content is empty
    }
    if (!videoUrl.trim()) {
        alert("Video url cannot be empty")
        return;
    }
    
    const token = getSessionToken();
    const headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    };

    const data = {
        subject: subject,
        title: title,
        video_url: videoUrl
    };

    try {
        const response = await fetch("/api/v1/videos", {
            method: "POST",
            headers: headers,
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Video posted successfully");
            // Clear and hide the form
            document.getElementById("video-subject").value = "Architecture"; // Reset the subject
            document.getElementById("video-title").value = ""; // Clear the content
            document.getElementById("video-url").value = ""; // Clear the content
            document.getElementById("post-video-form").classList.add("hidden");
            loadVideos(subject);
        } else {
            const errorData = await response.json();
            alert("Error posting video: " + errorData.error);
        }
    } catch (error) {
        console.error("Error posting video:", error);
    }
});

$(document).ready(function () {
    $('#search-icon').on('click', function () {
        $('#search-input').toggleClass('hidden');
    });

    $('#search-button').on('click', function () {
        // Get the search text from the input
        const searchText = $('#search-text').val().trim();

        // Perform AJAX request for global search
        $.ajax({
            url: `/api/v1/videos/search/${searchText}`,
            type: 'GET',
            dataType: 'json',
            success: function (data) {
                // Update the content of the vid-middle div with the search results
                updateVideoList(data.videos);
                $('#search-input').addClass('hidden');
            },
            error: function (error) {
                console.error('Error performing search:', error);
            }
        });
    });
});
