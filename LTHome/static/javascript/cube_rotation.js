$(document).ready(function() {
    // Wenn ein Button mit der Klasse animate geklickt wird
    $(".animate_cube").click(function() {
        // Bestimmen welcher Button geklickt wird
        var sectionname = this.name;
        var scene = document.querySelector("#" + sectionname + " .scene");
        $("#" + sectionname).find(".cube__face--top").css('display', 'block');
        $("#" + sectionname).find(".cube__face--bottom").css('display', 'block');
        setTimeout(() => {
            $("#" + sectionname).find(".cube__face--top").css('display', 'none');
            $("#" + sectionname).find(".cube__face--bottom").css('display', 'none');
        }, 1000);
        // Bestimmen welche Seite gerade nach vorne zeigt
        if (scene.classList.contains("show-back")) {
            // Auf die andere Seite drehn
            rotateCubeGoFront(sectionname);
        } else {
            // Auf die andere Seite drehn
            rotateCubeGoBack(sectionname);
        }
    });

    function rotateCubeGoFront(sectionname) {
        // Cube nach vorne drehn indem eine Css-Klasse hinzugefügt wird
        var subCnt = document.querySelector("#" + sectionname);
        var scene = subCnt.querySelector(".scene");
        scene.classList.remove("show-back");
        scene.classList.add("show-front");
    }

    function rotateCubeGoBack(sectionname) {
        // Cube nach hinten drehn indem eine Css-Klasse hinzugefügt wird
        var subCnt = document.querySelector("#" + sectionname);
        var scene = subCnt.querySelector(".scene");
        scene.classList.remove("show-front");
        scene.classList.add("show-back");
    }
})