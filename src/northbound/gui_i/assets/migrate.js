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
  
  let VM=function(){
    let name;
    // also contains a div property
  };
  VM.prototype.buildTemplate = function(){
    let heading = document.createElement('h3');
    let nameField = new InputField(this.name, 'name');
    let div = document.createElement('div');
    $(div).addClass("vmDiv");
    $(heading).html("VM").appendTo($(div));
    $(nameField.div).appendTo($(div));
    let removeButton = document.createElement('button');
    
    $(removeButton).html("Remove VM").appendTo($(div)).on('click',function(){
     if(confirm("Are your sure?")){
        $(div).remove();
     }
    });
    this.div = div;
  };
  
  let Migration = function(){
    let sourceCloud;
    let sourceSubnet;
    let destinationCloud;

  };
  Migration.prototype.buildTemplate = function(){
    this.div = document.createElement('div');
    $(this.div).addClass("migrationDiv");
    this.vmListDiv = document.createElement('div');
    
    let heading = document.createElement('h2');
    $(heading).html("Migration").appendTo($(this.div)); 
    
    let sourceCloudField = new InputField(this.sourceCloud, "source_cloud");
    $(sourceCloudField.div).addClass("source_cloud_heading").appendTo($(this.div));
    
    let sourceSubnetField = new InputField(this.sourceSubnet, "source_subnet");
    $(sourceSubnetField.div).addClass("source_subnet_heading").appendTo($(this.div));
    
    let destinationCloudField = new InputField(this.destinationCloud, "destination_cloud");
    $(destinationCloudField.div).addClass("destination_cloud_heading").appendTo($(this.div));
    

    $(this.vmListDiv).addClass("vmlist_heading").appendTo($(this.div));
    
    this.addVM();
    
    // button to add a VM
    let addVMButton = document.createElement('button');
    let self = this;
    $(addVMButton).addClass("addVM").on("click",function(){
      self.addVM();
    }).html("Add VM").appendTo($(this.div));
    
    let removeButton = document.createElement('button');
    $(removeButton).html("Remove Migration").appendTo($(this.div)).on('click',function(){
     if(confirm("Are your sure?")){
        $(self.div).remove();
     }
    });
  };
  Migration.prototype.addVM = function(){
    let v = new VM();
    v.buildTemplate();
    $(v.div).appendTo($(this.vmListDiv));
  };
  
  
  let VM_Migration = function(){};
  VM_Migration.prototype.buildTemplate = function(){
    this.div = document.createElement('div');
    $(this.div).addClass("vmMigrationDiv");
    this.migrationListDiv = document.createElement('div');
    
    let heading = document.createElement('h1');
    $(heading).html("Migration List").appendTo($(this.div)); 
    $(this.migrationListDiv).appendTo($(this.div));
    
    this.addMigration();
    
    // button to add a Subnet
    let addMigration = document.createElement('button');
    let self = this;
    $(addMigration).addClass("addMigration").on("click",function(){
      self.addMigration();
    }).html("Add Migration").appendTo($(this.div));
     let removeButton = document.createElement('button');
    $(removeButton).html("Remove Migration List").appendTo($(this.div)).on('click',function(){
     if(confirm("Are your sure?")){
        $(self.div).remove();
     }
    });
  }
  VM_Migration.prototype.addMigration = function(){
    let m = new Migration();
    m.buildTemplate();
    $(m.div).appendTo($(this.migrationListDiv));
  };


  let Box = function(){
  };
  Box.prototype.buildTemplate = function(){
    this.div = document.createElement('div');
    this.VMMigrationListDiv = document.createElement('div');
    $(this.VMMigrationListDiv).appendTo($(this.div));
    this.addVMMigration();
    let addVMMigration = document.createElement('button');
    let self = this;
    $(addVMMigration).addClass("addVMMigration").on("click",function(){
      self.addVMMigration();
    }).html("Add new set of migrations").appendTo($(this.div));
    
    this.submitBtn = document.createElement('button');
    $(this.submitBtn).addClass("submit").html("Submit").on("click",function(){
      if(confirm("Are you sure?")){
        // go thru everything and build a json
        let data = {};
        let VMMigrationList = $(".vmMigrationDiv");
        VMMigrationList.each(function(){
            let vmMigration = $(this);
            let name = "VM_Migration";
            let migrations = vmMigration.find(".migrationDiv");
            data[name] = [];
            migrations.each(function(){
                let migrationObj = {};
                migrationObj["VM"] = [];
                let vms = $(this).find(".vmDiv");
                vms.each(function(){
                    let props = $(this).find("div");
                    let obj = {};
                    props.each(function(){
                        let key = $(this).find(".fieldName").html();
                        let val = $(this).find(".spanVal").html();
                        obj[key] = val;
                    });
                    migrationObj["VM"].push(obj);
                });
                let sourceCloudHeading = $(this).find(".source_cloud_heading").find(".spanVal").html();
                migrationObj["source_cloud"] = sourceCloudHeading;
                let sourceSubnetHeading = $(this).find(".source_subnet_heading").find(".spanVal").html();
                migrationObj["source_subnet"] = sourceSubnetHeading;
                let destCloudHeading = $(this).find(".destination_cloud_heading").find(".spanVal").html();
                migrationObj["destination_cloud"] = destCloudHeading;
                data[name].push(migrationObj);
            });
        });
        
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
  Box.prototype.addVMMigration = function(){
    let c = new VM_Migration();
    c.buildTemplate();
    $(c.div).appendTo($(this.VMMigrationListDiv));
  }
  let b = new Box();
  b.buildTemplate();
  $(b.div).appendTo("#content");