import sys
import os
import yaml

arg = sys.argv
print(arg[1])
Yaml_file = arg[1]
with open(Yaml_file,'r') as stream:
    try:
        yaml_content = yaml.safe_load(stream)
        print(yaml_content)
        
        Cloud_Number = []
        for each in yaml_content:
            i = 0
            print(each)
            for item in yaml_content[each]:
                if len(item) > 0:
                    i = i + 1
            print(i)
            Cloud_Number.append(i)

        # Listing all number of subnets in the C1 and C2
        print("List of subnets in the C1:")
        print("--------------------------")

        C1S = []
        for x in range(0,Cloud_Number[0],1):
            subnet = str(yaml_content['C1'][x]['subnet_addr'])
            C1S.append(subnet)
            print(subnet)

        print("\n")
        print("List of subnets in the C2:")
        print("--------------------------")

        C2S = []
        for x in range(0,Cloud_Number[1],1):
            subnet = str(yaml_content['C2'][x]['subnet_addr'])
            C2S.append(subnet)
            print(subnet)

        print(C1S)
        print(C2S)

        compare_subnet_list_vxlan = []
        compare_subnet_list_gre = []
         
        for i in range(0,Cloud_Number[0],1):
            for j in range(0,Cloud_Number[1],1):
                if (C1S[i] == C2S[j]):
                    print("Entered in to the if loop")
                    test = str(C1S[i]) + ' - ' + str(C2S[j]) + ' - ' + 'VxLan'
                    print(test)
                    compare_subnet_list_vxlan.append(test)
                else:
                    test = str(C1S[i]) + ' - ' + str(C2S[j]) + ' - ' + 'GRE'
                    compare_subnet_list_gre.append(test)
    

        length = Cloud_Number[0] * Cloud_Number[1]
        
        len1 = len(compare_subnet_list_vxlan)
        len2 = len(compare_subnet_list_gre)
        
        if len1 > 0:
            for i in range(0,len1,1):
                print(compare_subnet_list_vxlan[i])
        if len2 > 0:
            for i in range(0,len2,1):
                print(compare_subnet_list_gre[i])
    
        # Writing the list in to the file
        path = '/home/ece792/LN_PROJECT/'
        file_path = '/home/ece792/LN_PROJECT/Compare_Subnets_Across_Clouds.yaml'
        try:
            if not os.path.exists(path):
                os.makedirs(path)
            else:
                print("The file path already exists: "+ str(path))

        except OSError:
            print ("Creation of the directory %s failed" % path)
        
        with open(file_path, 'w') as file:
            documents = yaml.dump(compare_subnet_list_vxlan, file, default_flow_style=False)
            documents = yaml.dump(compare_subnet_list_gre, file, default_flow_style=False)


#        with open('listfile.txt', 'w') as filehandle:
#            for items in C1S :
#                filehandle.write('%s\n' % items)
#            for items in C2S :
#                filehandle.write('%s\n' $ items)
    except yaml.YAMLError as exc:
        print(exc)

