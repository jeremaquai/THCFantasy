from PIL import Image





def rpgMainCharacterTopRow():
        filename = '_down_idle.png'
        relative_path = './assets/characters/rpgMainCharacter/'

    
        count = 1

        left = 0
        upper = 0
        right = 64
        lower = 64

        countdown = 4

        while countdown > 0:
            try:
                img = Image.open(f'{relative_path}{filename}')
                area = (left, upper, right, lower)
                img = img.crop(area)
                img.save(f'{relative_path}down_idle{count}.png')
            except IOError:
                print('Error')
                pass

            left = left + 64
            right = right + 64
            count += 1
            countdown -= 1 

def rpgMainCharacterBottomRow():
        filename = '_down_idle.png'
        relative_path = './assets/characters/rpgMainCharacter/'

    
        count = 5

        left = 0
        upper = 64
        right = 64
        lower = 128

        countdown = 1

        while countdown > 0:
            try:
                img = Image.open(f'{relative_path}{filename}')
                area = (left, upper, right, lower)
                img = img.crop(area)
                img.save(f'{relative_path}down_idle{count}.png')
            except IOError:
                print('Error')
                pass

            left = left + 32
            right = right + 32
            count += 1
            countdown -= 1 
def main():
    rpgMainCharacterTopRow()
    rpgMainCharacterBottomRow()


if __name__ == '__main__':
    main()

