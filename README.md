<h4>STEPS TO RUN THE PROJECT LOCALLY<h4>

<h6>STEP 1<h6>
<h6>CREATING POSTGRESS DATABASE USING DOCKOR CONTAINER<h6>
<div>
    <ul>
        <li>
            <p>Create a data directory for data volume mapping. Ex: /home/ukufu/data</p>
            <p>relative path for data storage= /home/ukufu/data</p>
        </li>
        <li>
            <p>Run below command for starting postgress docker container</p>
            <p>Make sure to replace the relative path</p>
            <p>sudo docker run -d --name ukufu_db -e POSTGRES_PASSWORD=password -v {relative path for data storage}:/var/lib/postgresql/data -p 5432:5432 postgres</p>
        </li>
    </ul>
</div>
<h6>STEP 2<h6>
    <h6>CLONING THE REPO<h6>
        <div>
            <ul>
                <li>
                    <p>git clone https://github.com/himanshir21/paranuara.git</p>
                </li>
                <li>
                    <p>cd paranuara/</p>
                </li>
            </ul>
        </div>
<h6>STEP 3<h6>
    <h6>SETTING UP THE ENVIRONMENT<h6>
        <div>
            <ul>
                <li>
                    <p>Run below commands in the project directory (paranuara).</p>
                </li>
                <li>
                    <p>If <em>pip</em> and <em>pipenv</em> is not installed then use below command for installation</p>
                    <p>sudo apt-get install python3-pip</p>
                    <p>More info for installation : https://www.makeuseof.com/tag/install-pip-for-python/</p>
                    <p>pip3 install pipenv</p>
                </li>
                <li>
                    <p>Activate virtual env using pipenv</p>
                    <p>pipenv shell</p>
                </li>
                <li>
                    <p>Installing dependencies</p>
                    <p>pipenv install</p>
                </li>
                <li>
                    <p>python manage.py makemigrations</p>
                </li>
                <li>
                    <p>python manage.py migrate</p>
                </li>
                <li>
                    <p>Loading data from json command</p>
                    <p>python manage.py process_companies</p>
                </li>
                <li>
                    <p>Running the server...</p>
                    <p>python manage.py runserver</p>
                </li>
            </ul>
        </div>
<h6>STEP 4<h6>
            <h6>APIs<h6>
                <div>
                    <ul>
                        <li>
                            <p>URL for the APIs..</p>
                            <p>http://127.0.0.1:8000/swagger/</p>
                        </li>
                    </ul>
                </div>
                
<h6>To run test cases<h6>
<p>python manage.py test<p>
        
                
