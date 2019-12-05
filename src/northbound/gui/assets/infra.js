let InputField = function(text, name){
  this.text = text;
  let div = document.createElement('div');
  let fieldName = document.createElement('span');
  $(fieldName).html(name).addClass("fieldName").appendTo($(div));
  let span = document.createElement('span');
  $(span).addClass("spanVal");
  let input = document.createElement('input');
  let edit = document.createElement('span');
  let self = this;
  $(input).addClass("hide");
  $(span).html(this.text);
  $(edit).html("Edit").on("click",function(){
    $(span).addClass("hide");
    $(edit).addClass("hide");
    $(input).val(self.text).removeClass("hide").focus();
  });
  $(input).on("blur",function(){
    if($(input).val().length>0){
      $(span).html($(input).val()).removeClass("hide");
      self.text = $(input).val();
      $(input).addClass("hide");
      $(edit).removeClass("hide");
    }
  });
  if(typeof text != 'undefined'){
    $(span).removeClass("hide");$(edit).removeClass("hide");
    $(input).addClass("hide"); 
  }else{
    $(span).addClass("hide");
    $(input).removeClass("hide"); $(edit).addClass("hide");
  
  }
  $(input).appendTo($(div));
  $(span).appendTo($(div));
  $(edit).appendTo($(div));
  this.div = div;
}
let SelectField = function(options, dispName){
  this.options = options;
  this.dispName = dispName;
  let div = document.createElement('div');
  let fieldName = document.createElement('span');
  $(fieldName).addClass("fieldName").html(dispName).appendTo($(div));
  let select = document.createElement('select');
  let last;
  for(var i in options){
    let option = options[i];
    let optionElement = document.createElement('option');
    last = optionElement;
    $(optionElement).val(option.val).html(option.html).appendTo($(select));
    last = $(optionElement);
  }
  last.attr("selected","selected");
  $(select).addClass("spanVal").appendTo($(div));
  this.div = div;
}

let VM=function(){
  let name;
  let disk;
  let mem;
  let vcpu;
  let internet_access;
  // also contains a div property
};
VM.prototype.buildTemplate = function(){
  let heading = document.createElement('h3');
  let nameField = new InputField(this.name, 'name');
  let diskField = new InputField(this.disk, 'disk');
  let memField = new InputField(this.mem, 'mem');
  let vcpuField = new InputField(this.vcpu, 'vcpu');
  let selectField = new SelectField([{val:true, html: "true"},{val:false, html:"false"}],'internet_access');
  let div = document.createElement('div');
  $(div).addClass("vmDiv");
  $(heading).html("VM").appendTo($(div));
  $(nameField.div).appendTo($(div));
  $(diskField.div).appendTo($(div));
  $(memField.div).appendTo($(div));
  $(vcpuField.div).appendTo($(div));
  $(selectField.div).appendTo($(div));
  let removeButton = document.createElement('button');
  
  $(removeButton).html("Remove VM").appendTo($(div)).on('click',function(){
   if(confirm("Are your sure?")){
      $(div).remove();
   }
  });
  this.div = div;
};

let Subnet = function(){
  let address;
};

Subnet.prototype.buildTemplate = function(){
  this.div = document.createElement('div');
  $(this.div).addClass("subnetDiv");
  this.vmListDiv = document.createElement('div');
  
  let heading = document.createElement('h2');
  $(heading).html("Subnet").appendTo($(this.div)); 
  let addressField = new InputField(this.address, "address");
  $(addressField.div).addClass("address_heading").appendTo($(this.div));
  $(this.vmListDiv).addClass("vmlist_heading").appendTo($(this.div));
  
  this.addVM();
  
  // button to add a VM
  let addVMButton = document.createElement('button');
  let self = this;
  $(addVMButton).addClass("addVM").on("click",function(){
    self.addVM();
  }).html("Add VM").appendTo($(this.div));
  
  let removeButton = document.createElement('button');
  $(removeButton).html("Remove Subnet").appendTo($(this.div)).on('click',function(){
   if(confirm("Are your sure?")){
      $(self.div).remove();
   }
  });
};
Subnet.prototype.addVM = function(){
  let v = new VM();
  v.buildTemplate();
  $(v.div).appendTo($(this.vmListDiv));
};

let Cloud = function(name){
  this.name = name;
  
}
Cloud.prototype.buildTemplate = function(){
  this.div = document.createElement('div');
  $(this.div).addClass("cloudDiv");
  this.subnetListDiv = document.createElement('div');
  
  let heading = document.createElement('h1');
  $(heading).html("Cloud").appendTo($(this.div)); 
  $(this.subnetListDiv).appendTo($(this.div));
  
  this.addSubnet();
  
  // button to add a Subnet
  let addSubnet = document.createElement('button');
  let self = this;
  $(addSubnet).addClass("addSubnet").on("click",function(){
    self.addSubnet();
  }).html("Add Subnet").appendTo($(this.div));
   let removeButton = document.createElement('button');
  $(removeButton).html("Remove Cloud").appendTo($(this.div)).on('click',function(){
   if(confirm("Are your sure?")){
      $(self.div).remove();
   }
  });
}
Cloud.prototype.addSubnet = function(){
  let s = new Subnet();
  s.buildTemplate();
  $(s.div).appendTo($(this.subnetListDiv));
};
let Box = function(){
};
Box.prototype.buildTemplate = function(){
  this.div = document.createElement('div');
  this.cloudListDiv = document.createElement('div');
  $(this.cloudListDiv).appendTo($(this.div));
  this.addCloud();
  let addCloud = document.createElement('button');
  let self = this;
  $(addCloud).addClass("addCloud").on("click",function(){
    self.addCloud();
  }).html("Add Cloud").appendTo($(this.div));
  
  this.submitBtn = document.createElement('button');
  $(this.submitBtn).addClass("submit").html("Submit").on("click",function(){
    if(confirm("Are you sure?")){
      // go thru everything and build a json
      let data = {};
      let clouds = $(".cloudDiv");
      let cloudLimit = Math.min(clouds.length,2); 
      for(var i=0;i<cloudLimit;i++){
        let cloud = $(clouds[i]);
        let cloudName = "C"+(i+1);
        let subnets = cloud.find(".subnetDiv");
        
        data[cloudName] = [];
        subnets.each(function(){
          let subnetObj = {};
          let address = $(this).find(".address_heading").find(".spanVal").html();
          subnetObj["subnet_addr"] = address;
          subnetObj["VM"] = [];
          
          let vms = $(this).find(".vmDiv");
          vms.each(function(){
            let props = $(this).find("div");
            let obj = {};
            props.each(function(){
              let key = $(this).find(".fieldName").html();
              let val;
              if($(this).children("select").length > 0){
                val = $(this).find("option:selected").val();
                val = val === 'true';
              }else{
                val = $(this).find(".spanVal").html();
              }
              obj[key] = val;
            });
            subnetObj["VM"].push(obj);
          });
          data[cloudName].push(subnetObj);
        });
      }
      console.log(data);
      $.ajax({
          url: "",
          type: "POST",
          data: JSON.stringify({"input": data}),
          contentType: "application/json",
          success: ()=>{alert("success");}
      });
    }
  }).appendTo($(this.div));
}
Box.prototype.addCloud = function(){
  let c = new Cloud();
  c.buildTemplate();
  $(c.div).appendTo($(this.cloudListDiv));
}
let b = new Box();
b.buildTemplate();
$(b.div).appendTo("#content");