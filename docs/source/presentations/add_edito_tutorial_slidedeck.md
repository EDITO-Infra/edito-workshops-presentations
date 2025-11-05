---
marp: true
paginate: true
theme: edito-marp
backgroundImage: url('../static/images/editobackgrounddark.png')
backgroundSize: cover
backgroundPosition: center
footer: '![Funded by the European Union](../static/images/footer-banner.png)'
title: Contributing an R Tutorial to EDITO Datalab
description: From R Markdown to a tutorial live on EDITO
class: lead
---

# 👋 Welcome!

## Contributing to EDITO Datalab

Learn how to contribute your knowledge to [**EDITO Tutorials** ](https://dive.edito.eu/training).

Presented by **Samuel Fooks**  
_Flanders Marine Institute (VLIZ)_

**For all the PDFs and code, check out the workshop [GitHub repository](https://github.com/EDITO-Infra/edito-workshops-presentations/tree/main)**

---

## Adding our tutorial to the [**EDITO Tutorials** ](https://dive.edito.eu/training)

<img src="https://github.com/EDITO-Infra/edito-workshops-presentations/blob/main/assets/images/editotutorialspage.png?raw=true">Tutorials</img>

---

# 🎯 What We'll Go Over

✅ How to become a contributor to EDITO tutorials
✅ Create a shareable tutorial   
✅ Share it publicly via **GitHub**  
✅ Launch it on **EDITO Datalab**  
✅ Register it using `tutorials.json`  
✅ Submit a **merge request**

All this is also covered in [EDITO Datalab Documentation](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/).

---

# Get an Account on EDITO

<div class="scrollable">

<span style="font-size: 1.5em; font-weight: bold; color: var(--accent-color);">🌐 Become a Beta Tester:</span>
<a href="https://edito-infra.eu/european-digital-twin-ocean-beta-testing-sign-up-form/" style="font-size: 1.2em; text-decoration: none; color: blue;">Sign up here</a>

<span style="font-size: 1.5em; font-weight: bold; color: var(--accent-color);">📧 Receive an Email:</span>
You will receive an email from the developer team with further instructions.


<span style="font-size: 1.5em; font-weight: bold; color: var(--accent-color);">🔑 Sign up to Mercator Ocean GitLab:</span>
<a href="https://gitlab.mercator-ocean.fr/users/sign_up" style="font-size: 1.2em; text-decoration: none; color: blue;">Create your account</a>

---

# Contribute to the Tutorials Content Repository

<span style="font-size: 1.5em; font-weight: bold; color: var(--accent-color);">🔗 Access Repositories:</span>
Once your account is created, you will be added as a developer to the following repositories:
<ul>
  <li><a href="https://gitlab.mercator-ocean.fr/pub/edito-infra/service-playground" style="font-size: 1.2em; text-decoration: none; color: blue;">Service Playground Repository</a></li>
  <li><a href="https://gitlab.mercator-ocean.fr/pub/edito-infra/process-playground" style="font-size: 1.2em; text-decoration: none; color: blue;">Process Playground Repository</a></li>
  <li><a href="https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content" style="font-size: 1.2em; text-decoration: none; color: blue;">Tutorial Content Repository</a></li>
</ul>

<!-- <img src='../assets/images/editogitlabtutorials.png'>Tutorials Git Lab</img> -->
</div>

---

# 🧱 I have a new tool/script to share


✅ For example, I’ve written a tutorial in `.Rmd`:

- It explains how to use a tool or perform a task  
- Includes **Markdown** text and **R code chunks**  
- Shows plots, tables, or results inline
- Has some interactivity/user interaction

---

# 🧱 Example: My Tutorial on Accessing EDITO STAC

#### Here in this repository 

##### [/add_tutorial/my_stac_r_tutorial/stac_r_tutorial.Rmd](https://github.com/EDITO-Infra/edito-workshops-presentations/blob/main/add_tutorial/my_stac_r_tutorial/stac_r_tutorial.Rmd)

<img src="../static/images/makingRmdtutorial.png?raw=true" alt="Making Rmd" />

---

# 📂 Recommended Folder Structure

- Not mandatory but on EDITO we need applications that are resilient and understandable for everyone
- Include a good README.md [makeareadme.com](https://www.makeareadme.com/)
- Data and other assets separate

```
my_stac_r_tutorial/
├── stac-r-tutorial.Rmd
├── data/
├── docker-compose.yml(*optional)
└── README.md
```

---

# 🌐 Create a Repository on your GitHub

- Go to [github.com](https://github.com)
- Click **New repository**
- Set it to **Public**

A demonstration on YouTube
Creating Your First GitHub Repository and Pushing Code [Youtube](https://youtu.be/f26KI43FK58)

---

# 💻 Push Your Local Code to Your Github

```bash
# Initialize Git in your local directory (if not already initialized)
git init
# Add all files to the staging area
git add .
git config user.name username
git config user.email usermail@mail.com
# Commit the changes
git commit -m "Initial commit"
# Add the remote origin
git remote add origin https://github.com/username/stac-r-tutorial.git
# Push the changes to GitHub
git branch -M main
git push -u origin main

```

Creating Your First GitHub Repository and Pushing Code [Youtube](https://youtu.be/f26KI43FK58)

---

# ⚙️ Make your deployment URL

[EDITO Services](https://datalab.dive.edito.eu/catalog/All)

**Access the Service Configuration**  
  - Choose a service from the Service Catalog appropriate for your Tutorial
  - ex. R Studio, Jupyter-python

**Add Your GitHub Repository**  
  - In the `GIT` section add the url to your tutorial's github repository in the Repository field

**Set Resource Limits**  
  - In the resources section, adjust CPU and memory limits as needed 
  - e.g., `1600m` for CPU, `5Gi` for memory

---

# Save Configuration and Test your tutorial

**Save the Configuration**  
  - Click **Save** to store your settings. 

**Copy the URL in your brower**[deployment_url](../static/images/deploymenturl.png?raw=true)
  - This is the link used to deploy your service and clone your github into the service

**Launch the Service**  
  - Use the **Launch** button to start the service with your configuration.

**Test Your Tutorial**  
  - Verify that the service clones your github, and your tutorial can be run
  - Does it install the right packages? 
  - Does it produce the output(s) you expect?

---

### [Configuring EDITO Service](../static/videos/configuretutorialservice.mp4)

<video src="../static/videos/configuretutorialservice.mp4" controls width="900"></video>

---

## Tutorials respository and the tutorials.json

In order to add our tutorial to the EDITO tutorials we need to add it to the `tutorials.json` list 

[https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content/tutorials.json](https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content/-/blob/main/tutorials.json)

We will clone this repository and add our tutorial to this list, using the the template provided in the README

---

# 🛠️ Clone the Tutorials Repository to your Local PC


🌐 **EDITO GitLab Tutorials**:  
  [https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content](https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content)

<br>

📂 **Clone the Repo**:
  ```bash
  git clone https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content.git
  ```
</div>

---

### [Cloning EDITO Tutorials Content](../static/videos/clonetutorialscontent.mp4)
<video src="../static/videos/clonetutorialscontent.mp4" controls width="800"></video>

---

# 🛠️ Make a new branch

<div class="scrollable">
  <span style="color: var(--accent-color); font-size: 1.5em;">🌿</span> **Create a New Branch**:

  ```bash
  git checkout -b my-new-tutorial-branch
  ```

  <span style="color: var(--accent-color); font-size: 1.5em;">📤</span> **Push the New Branch**:

  ```bash
  git push origin my-new-tutorial-branch
  ```

---

  ### [Make branch](../static/videos/makenewbranch.mp4)
  <video src="../static/videos/makenewbranch.mp4" controls width="800"></video>

---

## Add your tutorial to 'tutorials.json'

<span style="color: var(--accent-color); font-size: 1.2em;">🔗</span> <strong><a href="https://datalab.dive.edito.eu/launcher/ide/rstudio?name=myeditotutorialtest&version=2.3.1&s3=region-bb0d481d&resources.limits.cpu=%C2%AB1600m%C2%BB&resources.limits.memory=%C2%AB5Gi%C2%BB&git.name=%C2%AB%C2%BB&git.email=%C2%AB%C2%BB&git.repository=%C2%ABhttps%3A%2F%2Fgithub.com%2FEDITO-Infra%2Fedito-workshops-presentations%C2%BB" target="_blank" style="color: var(--accent-color); text-decoration: underline;">Deployment URL from previous step</a></strong>

<!--- fit -->
```json
{
    "name": {
        "en": "My New Tutorial"
    },
    "abstract": {
        "en": "A short description of your tutorial"
    },
    "authors": [
        "The authors and contributors"
    ],
    "types": [
        "types": [
          {
            "en": "Tutorial"
          }
    ],
    "tags": [
        "create", 
    ],
    "category": "training courses in data science",  // "What-If applications", "Focus applications", "training courses in data science"
    "imageUrl": "https://www.edito.eu/wp-content/uploads/2023/09/favicon.png",
    "articleUrl": {
        "en": "https://github.com/username/stac-r-tutorial", // Your github
    }
    "deploymentUrl": "https://datalab.dive.edito.eu/mydeployment.configuration.git.resources.etc"// DEPLOYMENT URL FROM PREVIOUS STEP
    // parts: [] 
}
```

---

### [Adding to tutorials.json](../static/videos/addtutorialjson.mp4)

Ex. A tutorial on accessing data via STAC in R and how to subset ARCO data.

<video src="../static/videos/addtutorialjson.mp4" controls width="800"></video>

---

## Push your updates onto your branch

```bash
# Stage all changes
git add .
# Commit the changes with a descriptive message
git commit -m "Added my awesome tutorial to tutorials.json"
# Push the changes to your branch
git push origin my-new-tutorial-branch
```

---

# 🔁 Create a Merge Request
- Check the gitlab https://gitlab.mercator-ocean.fr/pub/edito-infra/edito-tutorials-content
- See if your commit is in a pipeline and if it passes or not
- If it passes, create a Merge Request
- In your merge request, '@pub/edito-infra/codeowners' to request code owners to review your proposal.

---

# ✅ Final Review Checklist

✔️ Tutorial `.Rmd` created and runs  
➡️ GitHub repo is public and clean  
🔗 Launch link tested  
✅ `tutorials.json` updated
✅ Commited to Gitlab and passes Pipeline
✔️ Merge Request submitted

---

# 🙌 Done!

Once your Merge Request is approved
🎉 You’ve contributed to EDITO Datalab!  
Your tutorial is now one click away from reproducible research!  

💬 Issues? Email [edito-infra-dev@mercator-ocean.eu](mailto:edito-infra-dev@mercator-ocean.eu)  
🔗 [Contribution Docs](https://pub.pages.mercator-ocean.fr/edito-infra/edito-tutorials-content/#/Contribution/tutorials)