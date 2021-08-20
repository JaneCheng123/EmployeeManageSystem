function loadPage(tree) {
      

      var tag = document.getElementById("allList");
      var uls = formTree(tree,"default",0);
      tag.appendChild(uls);
      var checkbox = document.getElementsByClassName("selected");
      var id = 1;
      Array.prototype.forEach.call(checkbox,function(el) {
          el.id = "selectedDept"+id.toString();
          el.name = "selectedDept"+id.toString();
          el.setAttribute("onclick","selectOne("+ id +")");
          id = id + 1;
      });


      console.log(uls);
}
function findChildren(tree,node) {
    var list = []
    for(var i = 0; i < tree.length; i++) {
        var sub = node + "/" + tree[i].deptcode;
        if(tree[i].deptcode != node && tree[i].pathcode.indexOf(sub) != -1) {
          // console.log(tree[i].deptcode);
          list.push([tree[i].deptcode,tree[i].name]);
        }
    }
    return list;
}

function findUser(tree,deptname) {
    var users = null;
    Array.prototype.forEach.call(tree,function(each) {
        if(each["name"] == deptname) {
            console.log(each["user"]);
            users = each["user"];
        } 
    });
    return users;
}

function formTree(tree,node,first) {
    var ul = document.createElement("ul");
    if(first != 0) {
      ul.style.display = "none";
    }
    var grandson = null;
    var children = findChildren(tree,node);
    for(var i = 0; i < children.length; i++) {
        var li = document.createElement("li");
        var a = document.createElement("A");
        a.setAttribute("href","#");
        a.innerText = children[i][1];
        a.onclick = getCode;
        
        li.appendChild(a);

        ul.appendChild(li);
        if (findChildren(tree,children[i][0]).length > 0) {
            a.setAttribute("class" ,"dropdown-toggle");
            a.ondblclick = dropDown;
            grandson = formTree(tree,children[i][0],1);
            ul.appendChild(grandson);
        }
    }
    users = findUser(tree,node);
    console.log(node);
    if(users && users.length > 0) {
        for(var i = 0; i < users.length; i++) {
            var li = document.createElement("li");
            var a = document.createElement("A");
            a.setAttribute("href","#");
            a.innerText = users[i];
            

            var check = document.createElement("input");
            check.type = "checkbox";
            check.className = "selected";

            check.value = users[i];
            li.appendChild(check);
            li.appendChild(a);
            ul.appendChild(li);

        }
    }
    return ul;
}

function dropDown(event) {
  var tag = event.target;

  tag = tag.parentElement.nextSibling;
  var state = tag.style.display;
  if (state && state=="none")
    tag.style.display = "block";
  else
    tag.style.display = "none";

  var deptcode = tag.value;
  console.log(deptcode);
}

function getCode(event) {
  var tag = event.target;
  console.log(tag.innerText);
}

function selectOne(id) {
  var checkbox = document.getElementsByClassName("selected");
  Array.prototype.forEach.call(checkbox,function(el) {
      el.checked = false;
  });
  document.getElementById("selectedDept"+id.toString()).checked = true;
  console.log(document.getElementById("selectedDept"+id.toString()).value);

  var deptvalue = window.parent.document.getElementsByName("deptcode");
  deptvalue.value = document.getElementById("selectedDept"+id.toString()).value;

}