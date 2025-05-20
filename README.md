---

This document explains how to deploy an image from Docker Hub using Kubernetes.

---

## Enabling Kubernetes in Docker Desktop

1. Open **Docker Desktop**.
2. Go to **Settings → Kubernetes**.
3. Check **"Enable Kubernetes"**.
4. Wait for it to show **"Kubernetes is running"** in the bottom status bar.

---

## Kubernetes YAML File 

### `password-checker-deployment.yaml`

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: password-checker-deployment
  labels:
    app: password-checker
spec:
  replicas: 1
  selector:
    matchLabels:
      app: password-checker
  template:
    metadata:
      labels:
        app: password-checker
    spec:
      containers:
      - name: password-checker-container
        image: sivanandhini23/password-checker
        ports:
        - containerPort: 8081
---
apiVersion: v1
kind: Service
metadata:
  name: password-checker-service
spec:
  type: NodePort
  selector:
    app: password-checker
  ports:
    - port: 8081
      targetPort: 8081
      nodePort: 30092
```

### Explanation of the YAML File

#### Deployment Configuration

1. **apiVersion: apps/v1**
   - Specifies the API version used to create the deployment.

2. **kind: Deployment**
   - Indicates that this YAML file is defining a Deployment resource.

3. **metadata:**
   - **name: password-checker-deployment**
     - The name of the deployment is `password-checker-deployment`.
   - **labels:**
     - **app: password-checker**
       - Labels used to identify the deployment.

4. **spec:**
   - **replicas: 1**
     - Specifies that one replica (or instance) of the application should be running.
   - **selector:**
     - **matchLabels:**
       - **app: password-checker**
         - This label is used to identify the pods managed by this deployment.
   - **template:**
     - **metadata:**
       - **labels:**
         - **app: password-checker**
           - Labels applied to the pods created by this deployment.
     - **spec:**
       - **containers:**
         - **name: password-checker-container**
           - The name of the container.
         - **image: sivanandhini23/password-checker**
           - The Docker image used for the container.
         - **ports:**
           - **containerPort: 8081**
             - The port on which the container listens.

#### Service Configuration

1. **apiVersion: v1**
   - Specifies the API version used to create the service.

2. **kind: Service**
   - Indicates that this YAML file is defining a Service resource.

3. **metadata:**
   - **name: password-checker-service**
     - The name of the service is `password-checker-service`.

4. **spec:**
   - **type: NodePort**
     - The type of service, which exposes the service on each Node's IP at a static port.
   - **selector:**
     - **app: password-checker**
       - This label is used to select the pods that the service will expose.
   - **ports:**
     - **port: 8081**
       - The port on which the service is exposed.
     - **targetPort: 8081**
       - The port on the container to which the service forwards traffic.
     - **nodePort: 30092**
       - The static port on each Node's IP where the service is exposed.

---

## Running the Application

1. **Apply the Deployment and Service:**
   ```sh
   kubectl apply -f password-checker-deployment.yaml
   ```

2. **Check the Status:**
   ```sh
   kubectl get deployments
   kubectl get services
   ```

3. **Access the Application:**
   Open the browser and go to `http://localhost:30092/verify-password/`.

---
