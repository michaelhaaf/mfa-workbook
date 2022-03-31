form Variables
    sentence filename
endform
Read from file... 'filename$'
Resample... 16000 50
nowarn Write to WAV file... 'filename$'
nocheck Remove
