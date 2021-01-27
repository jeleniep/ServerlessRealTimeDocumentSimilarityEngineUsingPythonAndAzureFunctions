# Simgine deployment

1. Create resource group

```Bash
az group create \
  --name SimgineNew \
  --location "UK West"
```

2. Create resources
```Bash
templateFile="./azuredeploy.json"
az deployment group create \
  --name SimgineTemplate \
  --resource-group SimgineNew \
  --template-file $templateFile
```
3. Deploy function Simgine from "azure/Simgine" using from Visual Studio Code.
   
