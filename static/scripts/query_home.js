function submit_search() {

    var restaurant = document.getElementById("restaurant");
    
    var restaurant_detail = {
      restaurant_name: restaurant.value,
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
            var restaurant_name = document.getElementById("restaurant_name");
            restaurant_name.innerHTML = restaurant.value;
          }  
        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
      });

  }

  function submit_item(){
    var restaurant_name = document.getElementById("restaurant");
    var menu_name = document.getElementById("menu_name");
    var description = document.getElementById("description");
    var course = document.getElementById("course");
    var price = document.getElementById("price");

    console.log(restaurant_name.value)
    var menu_item = {
      restaurant_name: restaurant_name.value,
      item_name: menu_name.value,
      description: description.value,
      course: course.value,
      price: price.value,
    }

    fetch(`${window.origin}/new_item`, {
      method: "POST",
      credentials: "include",
      body: JSON.stringify(menu_item),
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
          var submit_response = document.getElementById("submit_response");
          submit_response.innerHTML = data["message"];
        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
      });
  }