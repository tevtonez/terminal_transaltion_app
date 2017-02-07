# -*- coding: utf-8

def instructions():

  text_separator = "*"* 20

  print "\n{} Greetings! {}\n".format(text_separator,text_separator)

  print 'You\'ve started Pytranslator v. 0.0.3\n\n\
This program allows you to load the txt file with english text, then \n\
translate it by one line at a time and then save your work (translated text\n\
and dictionary) in resulting txt files.\n'
  print "{} instructions {}\n".format(text_separator,text_separator)

  print "1. Run the proram.\n2. Copy original file into folder 'in'\n3. Type the relative path to your txt file (eg in/myfile.txt)\n4. Start translating the lines.\n5. Every fully translated segment will be saved into the folder named 'out' automatically.\n6. Every words pair is saved instantly into dictionary fiel in 'out' folder.\n7. You can always quit by typing exactly 'CQuit': your progress will be automatically saved."
  print text_separator,text_separator,text_separator



import sys, os, io
reload(sys)
sys.setdefaultencoding('utf-8')



def Quitting_app(rawinput_text):
  if rawinput_text == "CQuit":
    import sys
    sys.exit(0)




def load_file():
  """this asks user for a file path and loads the txt file; then returns the list with lines as the line items"""

  file_path = raw_input('Введите имя файла для перевода:')

  # quitting if user desires
  Quitting_app(file_path)

  file_name =  os.path.split(file_path)[-1]

  with io.open(file_path, 'r') as a_file:
    text_by_lines = [line.rstrip() for line in a_file]

  return text_by_lines, file_name




def Reading_from_Save(file_name):
  """this loads the word pairs from dictionary 'file_name' and returns a dictionary 'dictionary'"""

  last_translated_segment = 0

  if os.path.exists('out/save_{}'.format(file_name)):
    with io.open('out/save_{}'.format(file_name)) as save_file:
      last_translated_segment = save_file.read()

  return last_translated_segment




def Reading_from_Dictionary(file_name):
  """this loads the word pairs from dictionary 'file_name' and returns a dictionary 'dictionary'"""

  dictionary = dict()

  if os.path.exists('out/dic_{}'.format(file_name)):
    with io.open('out/dic_{}'.format(file_name)) as dictionary_file:

      for line in dictionary_file:

        (k, v) = line.strip().split("=")
        dictionary[k] = v

  return dictionary




def  auto_translation(cur_sentence, dictionary):
  """this auto translate passed 'cur_sentence' usign word pairs form dictionary"""

  aut_tanslated_setence = ''

  cur_sentence = cur_sentence.split()

  for word in cur_sentence:

    if word in dictionary.keys():
      translated_word = dictionary[word]
      aut_tanslated_setence += translated_word + ' '

    else:
     aut_tanslated_setence += word + ' '

  return aut_tanslated_setence




def need_to_translate(cur_sentence, file_name, dictionary, num_of_segment):
  """this verifies if the line 'cur_sentence' needs the translation and asks user to enter the translation for every word in the line"""

  sentence_len = len(cur_sentence)
  translated_line = ''

  for word in cur_sentence:
    word = word.lower()


    if word not in dictionary.keys():
      word_translation = raw_input('Переведите слoво "{}": '.format(word))

      # quitting if user desires
      Quitting_app(word_translation)

      dictionary[word] = str(word_translation)

      if word_translation ==  '' :
        dictionary[word] = " "

      # compiling a line to be written into a dictionary
      dict_line = "{}={}\n".format(word, dictionary[word])

      #writing a line into dictionary file
      with io.open('out/dic_{}'.format(file_name), 'a') as dictionary_file :
        dictionary_file.write(dict_line.decode('utf-8'))

      # compiling translated line of text to be written into a translated file
      if word_translation > '' or word_translation > ' ':
        translated_line += ''.join(word_translation) + " "

    else:
      translated_line += ''.join(dictionary[word]) + " "


  # writing translated line into translated file
  translated_line = translated_line + "\n"
  with io.open('out/trans_{}'.format(file_name), 'a') as translatoin_file :
    translatoin_file.write(translated_line.decode('utf-8'))

  # saving progress (segment)
  num_of_segment = str(num_of_segment)
  with io.open('out/save_{}'.format(file_name), 'w') as translatoin_file :
    translatoin_file.write(num_of_segment.decode('utf-8'))





def translate(text):
  """this is a main function that takes segment of text 'text' and passess it to 'auto_translation', 'need_to_translate' functions"""

  current_sentence =[]
  num_of_segment = 0
  total_segments = len(text[0])
  file_name = text[1]

  # reading the progress if any
  last_translated_segment = Reading_from_Save(file_name)
  print "\nЗагружен последний сегмент: {}".format(last_translated_segment)

  # reading from dictionary
  dictionary = Reading_from_Dictionary(file_name)

  # If there is saved progress - load the last not translated segment
  if last_translated_segment > 0:
    next_segment_to_translate = int(last_translated_segment) + 1
    text_to_translate = text[0][next_segment_to_translate::]
    num_of_segment = next_segment_to_translate

  else:
    text_to_translate = text[0]

  # loading sentences
  for sentence in text_to_translate:

    num_of_segment += 1

    if len(sentence) > 0:
      current_sentence = sentence.lower().split(' ')

      print "Файл: {} / cегмент: {} из {}".format(file_name, num_of_segment, total_segments)

      # showing already translated words in dictionary
      print '\nАвто-перевод сегмента: {}'.format( auto_translation(sentence.lower(), dictionary) )

      # checking if the words in the sentence need translation and write them into dictionary if needed
      need_to_translate(current_sentence, file_name, dictionary, num_of_segment)







# run the app
instructions()
print translate( load_file() )






if __name__ == '__main__':
  main()


# Copyright (c) 2016, Konstantin Chernukhin, All rights reserved.
# Created as a part of learning and practicing process.
#
# Author's url: http://octogear.com
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# IABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
