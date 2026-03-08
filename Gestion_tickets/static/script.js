 
/*** aqui voy a poner los scripts 
 * 
 *  
 *  :V
 * 
 */


function updateDateTime() {
  const now = new Date();
  const date = now.toLocaleDateString('es-MX');
  const time = now.toLocaleTimeString('es-MX');
  document.getElementById("datetime").innerHTML = 
  "📅 " + date + " &nbsp;&nbsp; 🕒 " + time;
}
setInterval(updateDateTime, 1000);
updateDateTime();
