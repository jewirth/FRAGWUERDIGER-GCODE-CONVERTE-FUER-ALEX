import sys
import math

def getArgs():
    if (len(sys.argv) != 6):
        print('Da stimmt was mit den Argumenten nicht...')
        print('Syntax : python alex.py <gcode-file> <x-amp> <x-phase> <y-amp> <y-phase>')
        print('Example: python alex.py foo.gcode 1 0 1 0')
        sys.exit(1) 
    input_file  = sys.argv[1]
    amplitude_x = float(sys.argv[2])
    phase_x     = float(sys.argv[3])
    amplitude_y = float(sys.argv[4])
    phase_y     = float(sys.argv[5])
    return input_file, amplitude_x, phase_x, amplitude_y, phase_y

def convert(line, xpos, ypos, zpos, amplitude_x, phase_x, amplitude_y, phase_y):
    x_neu = xpos + amplitude_x * math.sin(zpos / 8 * 360 + phase_x)
    y_neu = ypos + amplitude_y * math.sin(zpos / 8 * 360 + phase_y)
    beginning_of_new_line = 'G1 X' + str((x_neu)) + ' Y' + str(y_neu)
    end_of_new_line = ''
    if len(line.split(' E')) == 2:
        end_of_new_line = ' E' + line.split(' E')[1]
    elif len(line.split(' F')) == 2:
        end_of_new_line = ' F' + line.split(' F')[1]
    else:
        end_of_new_line = '\n'
    return beginning_of_new_line + end_of_new_line

def main():
    print('******************************************')
    print('* FRAGWUERDIGER GCODE CONVERTE FUER ALEX *')
    print('******************************************')
    input_file, amplitude_x, phase_x, amplitude_y, phase_y = getArgs()
    file_in  = open(input_file,  'r')
    file_out = open(input_file + '_edited.gcode', 'w')
    xpos = ypos = zpos = 0
    new_line = ''
    line_counter1 = 0
    line_counter2 = 0
    for line in file_in:
        line_counter1 = line_counter1 + 1
        new_line = line
        if line.find('G1 Z') == 0:
            zpos = float(line[4:].split(' ')[0])
        elif line.find('G1 X') == 0:
            line_counter2 = line_counter2 + 1
            xpos = float(line[4:].split(' ')[0])
            ypos = float(line.split(' Y')[1].split(' ')[0])
            new_line = convert(line, xpos, ypos, zpos, amplitude_x, phase_x, amplitude_y, phase_y)
        file_out.write(new_line)
    print(str(line_counter1) + ' lines of gcode processed')
    print(str(line_counter2) + ' lines of gcode edited')

main()
