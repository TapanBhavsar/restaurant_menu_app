function create_item_child(item) {
    var div = document.createElement("div");

    div.innerHTML = `<br><br>
    <form id="${item.name}" action="" onsubmit="return false">
    <label for="menu_name">Menu Name:${item.name}</label>
    <input type="text"  name="menu_name" value="${item.name}" readonly><br>
    <label for="description">Description:</label>
    <input type="text"  name="description" value="${item.description}"><br>
    <label for="course">Course:</label>
    <input type="text"  name="course" value="${item.course}"><br>
    <label for="price">Price:</label>
    <input type="text"  name="price" value="${item.price}"><br>
    
    <button type="submit" form="${item.name}" onclick="update_item('${item.name}');">Update</button>
    <button type="submit" form="${item.name}" onclick="delete_item('${item.name}');">Delete</button>
    </form>`;
  
    document.getElementById("available_items").appendChild(div); 
}


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
          // console.log(data);
          if(data["message"] == "OK"){
            // TODO create html format for all results by adding into innerHTML or new div
            var available_menu_items = data["result"]
            available_menu_items.forEach(create_item_child);

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

function update_item(item){
    var restaurant_name = document.getElementById("restaurant");
    var item_form = document.getElementById(item);

    var menu_item = {
      restaurant_name: restaurant_name.value,
      item_name:  item_form.elements["menu_name"].value,
      description: item_form.elements["description"].value,
      course: item_form.elements["course"].value,
      price: item_form.elements["price"].value,
    }

    fetch(`${window.origin}/update_item`, {
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

  function delete_item(item){
    var restaurant_name = document.getElementById("restaurant");
    var item_form = document.getElementById(item);

    var menu_item = {
      restaurant_name: restaurant_name.value,
      item_name: item_form.elements["menu_name"].value,
    }

    fetch(`${window.origin}/delete_item`, {
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
          if (data.message == "done") {
            var div = document.getElementById(item);
            div.remove();
          }
        });
      })
      .catch(function (error) {
        console.log("Fetch error: " + error);
      });
  }
