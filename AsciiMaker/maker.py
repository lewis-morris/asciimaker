import numpy as np
import cv2
from IPython.display import HTML

class AsciiCreator:

    def __init__(self, w_size=800, colour=True, background=True, invert=False, output="html", block_size=10,
                 characters=".,:-=+>coO08&%@#", font="Cousine", font_multiplier=1):
        """
        Used to create ASCII art images

        params:

        w_size: (int) the size of the output art. Is just a general size and not pixels. Good ranges are 1000-2000
        colour: (bool) To use colour or not. True == Colour text False == Greyscale
        background: (bool) To colour the background or not.
        invert: (bool) If True all colour are inverted
        block_size: (int) Increase or decrease this value to change the amount of characters per image. Lower numbers make the image more complex (higher definition)
        characters: (string) The characters to use to construct the image. Ordered from lowest to hightest intensity i.e the first character is lighter colours, the last one is darker.
        font: (String) A google fonts name, full list found here  "https://fonts.google.com/?category=Monospace".
        font_multiplier: (float) times the font size by the amount
        """

        self.w_size = w_size
        self.colour = colour
        self.background = background
        self.output = output
        self.block_size = block_size
        self.chars = characters
        self.invert = invert
        self.font = font
        self.font_multiplier = font_multiplier

    def set_image(self, img_path, arr=False):
        """Used to set base image
        params:

        img_path: (string) The file path of the input image.

        """
        if arr is False:
            img = cv2.imread(img_path)
        else:
            img = img_path

        if img is None:
            raise ("Image file not found")
        h, w, _ = img.shape
        diff = h / w
        self.image = cv2.resize(img, (int(self.w_size), int(self.w_size * diff)))
        self.grey = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY).copy()

    def _get_char(self, val):

        con = 255 / len(self.chars)
        cur_con = con
        cur_let = 0
        while True:
            if val <= cur_con:
                return self.chars[cur_let]
            cur_con += con
            cur_let += 1

    @staticmethod
    def _get_hex(b, g, r):

        return '#%02x%02x%02x' % (r, g, b)

    def create(self,lines_only=False):

        # get intensity of greyscale
        whole_intensity = abs(self.grey[:, :].mean() - (255 if self.invert else 0))

        # set block sizes
        x_block_size = self.block_size
        # set y block sizes - this is different because images were not generating with the correct aspect ratio
        y_block_size = int(x_block_size * 1.75)
        # set font size
        self.fontsize = int(22 * (x_block_size / 15))
        # set inital positions
        current_x = 0
        current_y = 0

        # get the background hex color
        back_hex = self._get_hex(int(whole_intensity), int(whole_intensity), int(whole_intensity))

        #set var to hold html
        top = ""
        # loop x axis
        lines = [""]
        while True:
            # get average pixel value
            averageR = abs(
                self.image[current_y:current_y + y_block_size, current_x:current_x + x_block_size, 2].mean() - (
                    255 if self.invert else 0))
            averageG = abs(
                self.image[current_y:current_y + y_block_size, current_x:current_x + x_block_size, 1].mean() - (
                    255 if self.invert else 0))
            averageB = abs(
                self.image[current_y:current_y + y_block_size, current_x:current_x + x_block_size, 0].mean() - (
                    255 if self.invert else 0))
            # get block intensity
            intensity = abs(self.grey[current_y:current_y + y_block_size, current_x:current_x + x_block_size].mean() - (
                255 if self.invert else 0))

            # calc background if needed
            background = f"; background-color:{back_hex}" if self.background else f"; background-color:#000000" if not self.background and self.invert else ""

            # calc color if needed
            colour = f"color:{self._get_hex(int(averageB), int(averageG), int(averageR))}" if self.colour else f"color:{self._get_hex(int(intensity), int(intensity), int(intensity))}"

            # write to list
            lines[-1] += f'<span style=" {colour} {background} "><strong>{self._get_char(intensity)}</strong></span>'

            # increment the block size to move position
            current_x += x_block_size

            # if overspill image edge then drop down a line and reset x
            if current_x >= self.image.shape[1]:
                lines.append("<br/>")
                lines.append("")
                current_x = 0
                current_y += y_block_size

            # if overspil y axis break
            if current_y >= self.image.shape[0]:
                break

        # set font and hmtl header
        font_name = self.font.replace(" ", "+")

        if lines_only is False:
            top = f"<!DOCTYPE html><html><head><link href='https://fonts.googleapis.com/css?family={font_name}' rel='stylesheet'><style>body {{    font-family:  '{self.font}' ;font-size: {int(self.fontsize*self.font_multiplier)}px;}}</style></head><body>"

        # write lines
        for ln in lines:
            top += ln

        if lines_only is False:
            # finalise html
            top += "</body></html>"

        # set to obj var
        self.final = top

    def write_html(self,image_path, output):

        """
        Used to create the output html.

        Params:
        image_path: (string) The image path of the file to be converted
        output: (string) Define the output path of HTML file

        """
        self.set_image(image_path)
        self.create()

        if type(output) == str:
            f = open(output, "w")
            f.write(self.final)
            f.close()
        else:
            raise("Must pass string")

    def write_gif(self, gif_path, output, frame_time):

        """
        Used to create the output html.

        Params:
        image_path: (string) The image path of the file to be converted
        output: (string) Define the output path of HTML file
        frame_time: (int) time in miliseconds between frames
        """

        font_name = self.font.replace(" ", "+")

        cap = cv2.VideoCapture(gif_path)

        i=0

        html = ""

        while (True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if frame is None:
                break
            self.set_image(frame,True)
            self.create(True)
            html += f"<div id={i} hidden='true'>{self.final}</div>"
            i +=1


        html =  f"<!DOCTYPE html><html><head><link href='https://fonts.googleapis.com/css?family={font_name}' rel='stylesheet'><style>body {{    font-family:  '{self.font}' ;font-size: {int(self.fontsize*self.font_multiplier)}px;}}</style></head><body><h1 hidden='' id=loading>Loading</h1>" + html
        html += """

<script>
function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
}

function show(){
    var total = document.getElementsByTagName("body")[0].getElementsByTagName("div").length-1
    for(const x in document.getElementsByTagName("body")[0].getElementsByTagName("div")){
        if(document.getElementById(x).hidden == ""){
            if(x==total){
                document.getElementById("0").hidden = ""
            }else{
                document.getElementById(parseInt(x)+1).hidden = ""
            }            
            document.getElementById(x).hidden = "true"
            return
        }
    }
}

function animate(){
    setInterval(() => { show() ; }, """ + str(frame_time) + """);
}
function unhide_first(){
    document.getElementById("0").hidden = ""
}

window.onload = () => {unhide_first(); animate() }

</script>
</body>
</html>"""

        if type(output) == str:
            f = open(output, "w")
            f.write(html)
            f.close()
