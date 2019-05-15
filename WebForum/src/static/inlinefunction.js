function fgettopics() {
        var jsvuserid = getUrlVars()["userid"];
        $.ajax({
              url: "{{ url_for('gettopics') }}",
              data: { userid: jsvuserid },
              success: function(result){

                document.getElementById("pageholder").innerHTML = result;
        }});
    }

    function getUrlVars()
    {
        var vars = [], hash;
        var hashes = window.location.href.slice(window.location.href.indexOf('?') + 1).split('&');
        for(var i = 0; i < hashes.length; i++)
        {
            hash = hashes[i].split('=');
            vars.push(hash[0]);
            vars[hash[0]] = hash[1];
        }
        return vars;
    }

    $( document ).ready(function() {
        fgettopics();
    });

    $("#topicpage").click(function(){
        $.ajax({
                url: "{{ url_for('topicpage') }}",
                success: function(result){
                document.getElementById("pageholder").innerHTML = result;
                document.getElementById("contentheader").innerHTML = "";
        }});
    });

    $("#topics").click(function(){
        fgettopics();
        document.getElementById("contentheader").innerHTML = "<strong> Welcome" + $("#hiddenusername").val() + " !!! </strong>";
    });

    $("#userprofile").click(function(){
        var vuserid = getUrlVars()["userid"];
        $.ajax({
              url: "{{ url_for('userprofile') }}",
              type: 'get',
              data: { userid: vuserid },
              success: function(result){
                document.getElementById("pageholder").innerHTML = result;
                document.getElementById("contentheader").innerHTML = "<strong>Update Profile</strong>";
        }});
    });

    $("#mytopics").click(function(){
        var vuserid = getUrlVars()["userid"];
        $.ajax({
              url: "{{ url_for('mytopics') }}",
              type: 'get',
              data: { userid: vuserid },
              success: function(result){
                document.getElementById("pageholder").innerHTML = result;
                document.getElementById("contentheader").innerHTML = "<strong>My Topics</strong>";
        }});
    });

    $("#myfavorites").click(function(){
        var vuserid = getUrlVars()["userid"];
        $.ajax({
              url: "{{ url_for('myfavorites') }}",
              type: 'get',
              data: { userid: vuserid },
              success: function(result){
                document.getElementById("pageholder").innerHTML = result;
                document.getElementById("contentheader").innerHTML = "<strong>My Favorites</strong>";
        }});
    });

    $("#pageholder").delegate( '#btncreatetopic', "click", function(event) {
        var jsVarTopic = $("#topicinput").val();
        var jsvuserid = getUrlVars()["userid"];
        $.ajax({
              url: "{{ url_for('createtopic') }}",
              type: 'post',
              data: { userid: jsvuserid,
                      topicname: jsVarTopic },
              success: function(result){
                document.getElementById("pageholder").innerHTML = result;
        }});
    });

    $("#banner").delegate( '#btnsearchtopic', "click", function(event) {
        var jsVSearchTopic = $("#searchinput").val();
        var jsvuserid = getUrlVars()["userid"];
        $.ajax({
              url: "{{ url_for('searchtopic') }}",
              type: 'get',
              data: { topicname: jsVSearchTopic,
                      userid: jsvuserid},
              success: function(result){
                document.getElementById("pageholder").innerHTML = result;
                $("#searchinput").val("");
                document.getElementById("contentheader").innerHTML = "<strong>Found Results</strong>";
        }});
    });

    function favoritefunc(vtopicid){
        var jsvuserid = getUrlVars()["userid"];
        var idelement = "emoji" + vtopicid;
        $.ajax({
              url: "{{ url_for('postfavorite') }}",
              type: 'post',
              data: { userid: jsvuserid,
                      topicid: vtopicid},
              success: function(result){
                if (result == "Added"){
                    $( "#" + idelement ).html( '<a href="javascript:favoritefunc(' + vtopicid + ')"><i class="em em-heart"></i></a>');
                 } else {
                    $( "#" + idelement ).html( '<a href="javascript:favoritefunc(' + vtopicid + ')"><i class="em em-orange_heart"></i></a>');
                 }
        }});
    }

    function getposts(ptopicid, ptopicname, pmin, pmax, pmaxrecords) {
        $("#hminindex").val(pmin);
        $("#hmaxindex").val(pmax);
        if (pmaxrecords === 'undefined'){
            $("#hmax").val("0");
        }else{
            $("#hmax").val(pmaxrecords);
        }
        $.ajax({
            url: "{{ url_for('getposts') }}",
            type: 'get',
            data: { topicid: ptopicid,
                    topicname: ptopicname,
                    minindex: pmin,
                    maxindex: pmax
                   },
            success: function(result){
               document.getElementById("pageholder").innerHTML = result;
               document.getElementById("contentheader").innerHTML = "<strong>Here are the posts for " + ptopicname + "</strong>";
        }});
    }

    function fpostcomnt(ptopicid, ptopicname){
        var inputcomment = $("#comment").val();
        var jsvuserid = getUrlVars()["userid"];
        var pmin = $("#hminindex").val();
        var pmax = $("#hmaxindex").val();
        var pmaxrecords = $("#hmax").val();

        $.ajax({
              url: "{{ url_for('postcomnt') }}",
              type: 'post',
              data: { topicid: ptopicid,
                      comments: inputcomment,
                      userid: jsvuserid},
              success: function(result){
               getposts(ptopicid, ptopicname, pmin, pmax, pmaxrecords);
               $("#comment").val("");
               document.getElementById("contentheader").innerHTML = "<strong>Here are the posts for " + ptopicname + "</strong>";
        }});
    }

    function pager(ptype, ptopicid, ptopicname, pminindex, pmaxindex, pmaxrecords) {

        if (ptype == "nxt"){
                pminindex = pmaxindex;
                pmaxindex = pmaxindex + 24;
                if (pminindex > pmaxrecords){
                    alert("No records found!!!");
                    return false;
                }
        } else {

                pminindex = pminindex - 24;
                pmaxindex = pmaxindex - 24;

                if (pminindex <= 0) {
                pminindex = 0
                pmaxindex = 24;
            }
        }

        $("#hminindex").val(pminindex);
        $("#hmaxindex").val(pmaxindex);
        $("#hmax").val(pmaxrecords);

        getposts(ptopicid, ptopicname, pminindex, pmaxindex, pmaxrecords);
    }

    $("#frame").delegate( '#modifybtn', "click", function(event) {
        var jsvuserid = getUrlVars()["userid"];
        vfirstname = $("#idfirstname").val();
        vlastname = $("#idlastname").val();
        vemail = $("#idemail").val();
        vusername = $("#idusername").val();
        vpassword = $("#idpassword").val();

        postData = {"userid": jsvuserid,
                    "wfirstname": vfirstname,
                    "wlastname":  vlastname,
                    "wemail":     vemail,
                    "wusername": vusername,
                    "wpassword": vpassword
                    };

        $.ajax({
              url: "{{ url_for('modifyuser') }}",
              data: postData,
              success: function(result){
               document.getElementById("pageholder").innerHTML = result;
        }});
    });