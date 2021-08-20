function dialogDept() {
    var box;
    var deptcode;
    var deptname;
    var callback;

    var self = this;

    this.init = function (box,deptcode,deptname,callback) {
        self.box = box;
        self.deptcode = deptcode;
        self.deptname = deptname;
        self.callback = callback;
    }

    this.showDialog = function () {
        console.log(this.deptname);
        var div = document.createElement('div');
        div.setAttribute("class","modal fade modal-dialog-scrollable show");
        div.setAttribute("id","staticBackdrop");
        div.setAttribute("data-bs-backdrop","static");
        div.setAttribute("data-bs-keyboard",false);
        div.setAttribute("tabindex","-1");
        div.setAttribute("aria-labelledby","staticBackdropLabel");
        div.setAttribute("aria-hidden","true");
        div.style.display = "block";
        
        var div1 = document.createElement('div');
        div1.setAttribute("id","modal-dialog");
        div1.setAttribute("class","modal-dialog");
        div.appendChild(div1);

        var div2 = document.createElement('div');
        div2.setAttribute("class","modal-content");
        div1.appendChild(div2);

        var div3 = document.createElement('div');
        div3.setAttribute("class","modal-header");
        var h5 = document.createElement('h5');
        h5.innerText = "Modal title";
        h5.class = "modal-title";
        h5.id = "staticBackdropLabel";
        div3.appendChild(h5);
        var btn = document.createElement('button');
        btn.setAttribute("class","btn btn-close");
        btn.setAttribute("type","button");
        btn.setAttribute("data-bs-dismiss","modal");
        btn.setAttribute("aria-label","Close");
        btn.setAttribute("onclick","closeModal()"); 
        div3.appendChild(btn);
        div2.appendChild(div3);

        var div4 = document.createElement('div');
        div4.setAttribute("class","modal-body");
        var div5 = document.createElement('div');
        div5.setAttribute("class","box");
        var iframe = document.createElement('iframe');
        iframe.setAttribute("src","account.do?$ACTION=deptmodal");
        iframe.setAttribute("scrolling","yes");
        iframe.setAttribute("width","350px");
        iframe.setAttribute("height","400px");
        iframe.setAttribute("id","modalcontent");
        iframe.setAttribute("name","modalcontent");
        div5.appendChild(iframe);
        div4.appendChild(div5);
        div2.appendChild(div4);

        var div6 = document.createElement('div');
        div6.setAttribute("class","modal-footer");
        var btn2 = document.createElement('button');
        btn2.setAttribute("class","btn btn-secondary");
        btn2.setAttribute("type","button");
        btn2.innerText = "Close";
        btn2.setAttribute("onclick","closeModal()"); 
        btn2.setAttribute("data-bs-dismiss","modal");
        div6.appendChild(btn2);
        var btn3 = document.createElement('button');
        btn3.setAttribute("class","btn btn-primary");
        btn3.setAttribute("type","button");
        btn3.setAttribute("data-bs-dismiss","modal");
        btn3.innerText = "Done";
        // btn3.setAttribute("onclick","dlg.getDept("+this.deptname+")"); 
        btn3.onclick = self.getDept;
        div6.appendChild(btn3);
        div2.appendChild(div6);
        document.body.appendChild(div);
    }


    this.getDept = function () {
        var iframe = document.getElementById("modalcontent");
        var checkbox = iframe.contentWindow.document.getElementsByClassName("selected");
        var input = document.getElementById(self.deptname);
        Array.prototype.forEach.call(checkbox,function(el) {
            if(el.checked == true) {
                 input.value = el.value;
            }
        });
        if (self.callback)
            eval(self.callback + "()");

    }
}


function selectDept(box,deptcode,deptname,cb) {
    var dlg = new dialogDept();
    dlg.init(box,deptcode,deptname,cb);
    dlg.showDialog();
}


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
        

        var check = document.createElement("input");
        check.type = "checkbox";
        check.className = "selected";

        check.value = children[i][1];
        li.appendChild(check);
        li.appendChild(a);

        ul.appendChild(li);
        if (findChildren(tree,children[i][0]).length > 0) {
            a.setAttribute("class" ,"dropdown-toggle");
            a.ondblclick = dropDown;
            grandson = formTree(tree,children[i][0],1);
            ul.appendChild(grandson);
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