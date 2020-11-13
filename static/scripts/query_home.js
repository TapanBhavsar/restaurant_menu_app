function submit_search() {

    var restaurant_name = document.getElementById("restaurant");
    
    var restaurant_detail = {
      restaurant_name: restaurant_name.value,
    };

    fetch(`${window.origin}/search`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(restaurant_detail),
      cache: "no-cache",
      headers: new Headers({
        "content-type": "application/json"
      })
    })
      .then(function (response) {
        if (response.status !== 200) {
          console.log(`Looks like there was a problem. Status code: ${response.status}`);
          return;
        }
        response.json().then(function (data) {
          console.log(data);
          if(data["message"] == "OK"){
            document.getElementById("new_item_entry").style.display= 'block'; // or none to remove
          }  
        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
      });

  }