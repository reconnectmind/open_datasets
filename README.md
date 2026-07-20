# Реестр открытых fNIRS-датасетов

Обновлено: 2026-07-20.

Каноническая таблица: [`public/registry.csv`](./public/registry.csv). Одна строка соответствует одному датасету или независимо скачиваемой части датасета. Основные сведения, счётчики и инвентарь сопутствующих признаков объединены в этом файле; репозитории и каталоги сами по себе в таблицу не включены.

## Просмотр

[`public/index.html`](./public/index.html) — самодостаточный SPA-просмотрщик поверх `registry.csv` (поиск, фильтры по источнику/лицензии/модальности/статусу, карточки-статистика, детальная панель с раскодированными признаками). `index.html` и `registry.csv` лежат рядом в `public/`, которая целиком публикуется на GitHub Pages.

Браузер блокирует чтение локального CSV через `file://`, поэтому локально запускать через сервер:

```bash
cd projects/reconnect/datasets/public
python3 -m http.server 8000
# открыть http://localhost:8000/index.html
```

## Деплой

`public/` автоматически публикуется на GitHub Pages воркфлоу [`.github/workflows/deploy-pages.yml`](./.github/workflows/deploy-pages.yml) при каждом пуше в `main` (или вручную через «Run workflow»). Первый запуск сам включает Pages (source = GitHub Actions).

## Схема

| Поле | Содержание |
| --- | --- |
| `dataset_key` | Стабильный локальный ключ `<source>:<id>` |
| `source`, `source_version` | Канонический источник и версия записи |
| `title`, `description` | Название источника и краткое фактическое описание |
| `population`, `n_subjects` | Популяция и число людей; пусто, если источник этого не подтверждает |
| `modalities` | Реально заявленные модальности |
| `paradigm` | Экспериментальная парадигма, нормализованная по README/статье; это не всегда BIDS `task` label |
| `task_description` | Подробное описание задания, условий и дизайна |
| `n_recordings` | Число независимо анализируемых сырых fNIRS-записей |
| `recording_count_basis` | Что именно посчитано и почему это считается отдельной записью |
| `fnirs_format` | Формат основной fNIRS-записи, отдельно от формата всего архива |
| `count_status` | `verified`, `partial`, `metadata-warning` или `unavailable` |
| `format`, `size` | Формат и размер опубликованного набора |
| `license` | Лицензия именно датасета, а не статьи или кода |
| `access_url`, `access_method` | Ссылка и способ получения |
| `metadata_status` | `verified-core`, `partial` или `metadata-warning` |
| `notes`, `evidence_url` | Ограничения интерпретации и первичный источник |
| `features_<group>` | Подтверждённые признаки группы вместе с форматом, уровнем привязки, статусом и основанием проверки |

Пустое значение означает «не подтверждено», а не «отсутствует».

### Единица записи

`n_recordings` — не число участников, trials, блоков или файлов в архиве. Это минимальная сырая единица, которую можно анализировать независимо:

- для BIDS NIRS — уникальный `participant × session × task × run` файл `*_nirs.snirf`;
- для NIRx — один согласованный stem из `.wl1/.wl2/.hdr/.evt/...`;
- для WFDB — одна запись `.dat + .hea`;
- для контейнеров и нестандартных архивов — отдельная participant/run-группа, только если структура это подтверждает.

Sidecars, `events.tsv`, производные данные и альтернативные разметки одного raw-файла не увеличивают счётчик. Например, в `ds007738` `longvisualorient` и `videoattend` дают две привязки событий к одной SNIRF-записи. Если удалённый file listing не позволяет проверить внутреннюю структуру без полной загрузки, `n_recordings` оставлено пустым.

Для всех 47 строк теперь задан проверяемый результат подсчёта: 34 счётчика подтверждены по file tree/manifest, 11 основаны на подтверждённой, но не полностью перечисленной структуре, а 2 имеют предупреждение о metadata. Ноль у `ds007477` означает отсутствие валидных raw-записей, а не неизвестное значение.

## Нормализованное представление

Сокращённая таблица ниже нужна для просмотра. `✓` означает проверенный file-level счётчик, `~` — частичный, `!` — предупреждение о metadata, `—` — подсчёт недоступен. Полный набор полей, основания счёта и точные URL находятся в `registry.csv`.

| Dataset | Источник / версия | Описание и парадигма | Популяция / N | Записи* | Модальности / формат | Размер | Лицензия | Доступ | Статус |
| --- | --- | --- | --- | ---: | --- | ---: | --- | --- | --- |
| `ds004514` | OpenNeuro 1.1.2 | Семантическое декодирование: называние и зрительное/слуховое/тактильное воображение | Не указана / 12 | 12 ✓ | EEG + fNIRS / BIDS 1.7.0 | 25.9 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds004514/versions/1.1.2) | verified-core; BIDS task labels `nirs`, `eeg` не описывают задачи |
| `ds004541` | OpenNeuro 1.0.0 | EEG-fNIRS во время общей анестезии, две сессии | Пациенты / 8 | 9 ✓ | EEG + fNIRS / BIDS 1.6.0 | 3.11 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds004541/versions/1.0.0) | verified-core |
| `ds004830` | OpenNeuro 2.0.0 | Декодирование пространственного внимания при анализе сложных сцен | Не указана / 12 | 14 ✓ | fNIRS / BIDS 1.7.1 | 1.32 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds004830/versions/2.0.0) | verified-core |
| `ds004973` | OpenNeuro 1.0.1 | Оценка риска пассажира в сценариях автоматизированного вождения | Не указана / 20 | 222 ✓ | fNIRS / BIDS 1.7.0 | 2.49 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds004973/versions/1.0.1) | verified-core; snapshot содержит 12 числовых task labels, статья описывает 14 сценариев |
| `ds005776` | OpenNeuro 1.0.1 | Электрическая/термическая стимуляция, tapping, imagery, rest | Не указана / 11 | 46 ✓ | fNIRS / BIDS 1.7.1 | 1.29 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds005776/versions/1.0.1) | verified-core |
| `ds005777` | OpenNeuro 1.0.1 | Болевая/тактильная стимуляция, morphine/placebo | Не указана / 14 | 113 ✓ | fNIRS / BIDS 1.7.1 | 907 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds005777/versions/1.0.1) | verified-core |
| `ds005929` | OpenNeuro 1.0.1 | Индуцированные двигательные артефакты | Не указана / 7 | 7 ✓ | fNIRS / BIDS 1.7.1 | 71.8 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds005929/versions/1.0.1) | verified-core |
| `ds005935` | OpenNeuro 1.0.0 | Наблюдаемые и выполняемые движения рук, motor complexity | Не указана / 21 | 64 ✓ | fNIRS / BIDS 1.8.0 | 774 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds005935/versions/1.0.0) | verified-core; legacy-архив Li2020mirror указывает другое N |
| `ds005963` | OpenNeuro 1.0.0 | FRESH Motor, четыре сессии | Не указана / 10 | 40 ✓ | fNIRS / BIDS 1.7.0 | 245 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds005963/versions/1.0.0) | verified-core |
| `ds005964` | OpenNeuro 1.0.0 | FRESH Audio | Не указана / 17 | 17 ✓ | fNIRS / BIDS 1.7.0 | 65.5 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds005964/versions/1.0.0) | verified-core |
| `ds006377` | OpenNeuro 1.0.2 | Влияние волос и характеристик кожи на качество fNIRS; rest и ball squeeze | Не указана / 115 | 690 ✓ | fNIRS / BIDS 1.8.0 | 1.48 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006377/versions/1.0.2) | verified-core |
| `ds006459` | OpenNeuro 1.0.0 | Word-color Stroop, sparse montage | Не указана / 17 | 17 ✓ | fNIRS / BIDS 1.8.0 | 177 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006459/versions/1.0.0) | verified-core |
| `ds006460` | OpenNeuro 1.0.0 | Word-color Stroop, high-density montage | Не указана / 17 | 17 ✓ | fNIRS / BIDS 1.8.0 | 482 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006460/versions/1.0.0) | verified-core |
| `ds006545` | OpenNeuro 1.0.0 | Test-retest time-domain fNIRS, auditory task | Не указана / 49 | 98 ✓ | fNIRS / BIDS 1.6.0 | 50.1 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006545/versions/1.0.0) | verified-core; заменяет удалённый дубль `ds006528` |
| `ds006673` | OpenNeuro 1.0.4 | Ball squeeze и resting state | Не указана / 17 | 67 ✓ | fNIRS / BIDS 1.8.0 | 8.35 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006673/versions/1.0.4) | metadata-warning: template text в references |
| `ds006902` | OpenNeuro 1.1.1 | Exercise-induced hypoalgesia, pain | Спортсмены и неспортсмены / 42 | 42 ✓ | fNIRS / BIDS 1.7.0 | 5.91 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006902/versions/1.1.1) | verified-core |
| `ds006903` | OpenNeuro 1.0.0 | Ball squeeze и resting state | Не указана / 17 | 67 ! | fNIRS / BIDS 1.8.0 | 5.83 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds006903/versions/1.0.0) | metadata-warning: незаполненные authors/references; связь с `ds006673` неясна |
| `ds007420` | OpenNeuro 1.0.4 | Multi-distance ball squeeze, motion-artifact induction, rest | Не указана / 12 | 60 ✓ | fNIRS / BIDS 1.7.1 | 588 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007420/versions/1.0.4) | verified-core; заменяет удалённый дубль `ds004929` |
| `ds007463` | OpenNeuro 1.1.1 | Валидация very-high-density DOT | Не указана / 8 | 88 ✓ | fNIRS + MRI / BIDS 1.11.0 | 74.4 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007463/versions/1.1.1) | verified-core; task labels закодированы |
| `ds007473` | OpenNeuro 1.0.0 | HD-DOT во время просмотра аудиовизуального фильма | Не указана / 5 | 189 ✓ | fNIRS / BIDS 1.11.0 | 39.0 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007473/versions/1.0.0) | verified-core; task labels закодированы |
| `ds007477` | OpenNeuro 1.0.1 | Placeholder-конверсия, задача `ort` не определена | Не указана / 18 в metadata | 0 ! | Невалидные SNIRF placeholders | 9.4 KB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007477/versions/1.0.1) | metadata-warning: raw fNIRS отсутствует |
| `ds007554` | OpenNeuro 1.0.0 | CMx7-MM: motor imagery, arithmetic, n-back, active/passive motor | Не указана / 30 | 519 ✓ | EEG + fNIRS + behavior / BIDS 1.8.0 | 4.52 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007554/versions/1.0.0) | verified-core |
| `ds007714` | OpenNeuro 1.0.0 | Visual task; научное описание отсутствует | Не указана / 64 | 64 ✓ | fNIRS / BIDS 1.10.0 | 1.34 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007714/versions/1.0.0) | metadata-warning: generic title и template references |
| `ds007719` | OpenNeuro 1.0.0 | Resting state; научное описание отсутствует | Не указана / 65 | 65 ✓ | fNIRS / BIDS 1.10.0 | 9.27 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007719/versions/1.0.0) | metadata-warning: generic title и template references |
| `ds007738` | OpenNeuro 1.0.0 | Whole-Head Cocktail Party: overt/covert attention, visual orienting, rest, video | Не указана / 38 | 199 ✓ | fNIRS / BIDS 1.7.1 | 38.8 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007738/versions/1.0.0) | verified-core |
| `ds007816` | OpenNeuro 1.0.1 | Semantic encoding и идентификация naturalistic movies через HD-DOT | Не указана / 6 | 178 ✓ | fNIRS + MRI / BIDS 1.11.0 | 138 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007816/versions/1.0.1) | verified-core; task labels закодированы |
| `ds007990` | OpenNeuro 1.0.0 | Изменения auditory cortex и субъективная тяжесть tinnitus | Не указана / 63 | 63 ✓ | fNIRS / BIDS 1.7.0 | 289 MB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds007990/versions/1.0.0) | verified-core |
| `ds008192` | OpenNeuro 1.0.0 | InterGenSynch, drawing task | Не указана / 122 | 725 ✓ | fNIRS / BIDS 1.7.0 | 2.79 GB | CC0 | [OpenNeuro](https://openneuro.org/datasets/ds008192/versions/1.0.0) | verified-core |
| `mental-fnirs` | PhysioNet 1.0 | 0/1/2-back: frontal fNIRS + TCD + behavior | Здоровые молодые взрослые / 14 | 12 ✓ | fNIRS + TCD / NIRx raw + CSV | 231 MB | PhysioNet CRHDL 1.5.0 | [PhysioNet](https://physionet.org/content/mental-fnirs/1.0/) | verified-core; также действует Data Use Agreement |
| `motion-artifact` | PhysioNet 1.0.0 | Чистые/загрязнённые движением fNIRS и EEG + accelerometry | Не указана / N не указан | 9 ✓ | fNIRS + EEG / CSV + WFDB | 649.9 MB | ODC Attribution 1.0 | [PhysioNet](https://physionet.org/content/motion-artifact/1.0.0/) | verified-core; 9 fNIRS и 23 EEG trials |
| `multimodal-nback-music` | PhysioNet 1.0.0 | 1/3-back под calming/exciting music | Не указана / 5 с fNIRS и core modalities | 5 ✓ | fNIRS + физиология + behavior / heterogeneous | 1.6 GB | ODC Attribution 1.0 | [PhysioNet](https://physionet.org/content/multimodal-nback-music/1.0.0/) | verified-core; 11 участвовали исходно |
| `neuro-stress-resilience-hci` | PhysioNet 1.0.0 | MATB-II baseline/stress/recovery | Взрослые / 35 | 35 ✓ | EEG + fNIRS + eye tracking + physiology | 19.1 GB | ODbL 1.0 | [PhysioNet](https://physionet.org/content/neuro-stress-resilience-hci/1.0.0/) | verified-core |
| `fNIRS2MW Visual` | Tufts current | Visual 0/1/2/3-back для mental-workload classification | Не указана / 87 total; 68 recommended | 87 ~ | fNIRS / raw + tabular windows | — | CC-BY-4.0 | [Box](https://tufts.box.com/s/1e0831syu1evlmk9zx2pukpl3i32md6r) | verified-core; рекомендуемая ML-выборка — 68 |
| `fNIRS2MW Audio` | Tufts current | Audio n-back для transfer/adaptive learning | Не указана / 53 total; 52 recommended | 53 ~ | fNIRS / raw + tabular windows | — | CC-BY-4.0 | [Box](https://tufts.box.com/s/t87j27ha7b7spitmtcm5nbltfnld5ekh) | verified-core; рекомендуемая ML-выборка — 52 |
| `sm7yt` | OSF current | Hyperscanning: social touch, emotional images, behavior и questionnaires | Женские пары friends/strangers / 94 (47 dyads) | 141 ~ | fNIRS / raw + preprocessed | — | CC-BY-4.0 | [OSF](https://osf.io/sm7yt/) | verified-core |
| `f6tdk` | OSF current | Passive auditory block design для сравнения analysis pipelines | Не указана / 17 по OpenfNIRS | 17 ~ | fNIRS / BIDS + SNIRF | — | Не указана | [OSF](https://osf.io/f6tdk/) | partial: OSF API не содержит license или N |
| `hygrip.h5` | Figshare v3 | Dynamic grip force: NIRS, EEG, EMG, force, respiration, eyes | Правши / 14 | 14 ~ | NIRS + EEG + physiology / HDF5 | 4.64 GB | MIT | [прямой HDF5](https://ndownloader.figshare.com/files/22837760) | verified-core; текущая лицензия записи отличается от CC-BY в статье |
| `7966830` | Zenodo 1.0.0 | Parkinson: finger tapping, walking, resting state | 20 PD + 20 controls / 40 | 120 ✓ | fNIRS / SNIRF в ZIP | 284 MB | CC-BY-4.0 | [прямой ZIP](https://zenodo.org/api/records/7966830/files/fNIRS_Parkinson.zip/content) | verified-core |
| `vesb-mh30` | Donders v1 | Automatic/non-automatic finger/leg movements, dual task | Не указана / 24 | 192 ✓ | fNIRS / BIDS + SNIRF | 2 GB | CC-BY-SA-4.0 | [DOI](https://doi.org/10.34973/vesb-mh30) | verified-core |
| `dans-zym-vewk` | DANS current | Resting-state FC, flourishing и subjective vitality | Не указана / 43 | 43 ~ | fNIRS / CSV + analysis files | — | Не указана | [DOI](https://doi.org/10.17026/dans-zym-vewk) | partial: DataCite rightsList пуст |
| `6575155` | Zenodo v0.0.1 | Малый BIDS-NIRS finger-tapping example | Не указана / 5 | 5 ~ | fNIRS / BIDS + SNIRF ZIP | 43.8 MB | `other-open` | [прямой ZIP](https://zenodo.org/api/records/6575155/files/rob-luke/BIDS-NIRS-Tapping-v0.1.0.zip/content) | verified-core; Zenodo классифицирует запись как software |
| `377b4ff8p6` | Mendeley v1 | Auditory/visual evoked activity у недавно имплантированных CI recipients | Adult CI / 12 | 12 ~ | fNIRS / BIDS + SNIRF | — | CC-BY-4.0 | [Mendeley](https://data.mendeley.com/datasets/377b4ff8p6/1) | partial: N подтвержден статьёй, file tree не перечислен |
| `crjdfn3g9` | Dryad v8 | Speech quiet/noise, audiovisual speech и lipreading | 46 CI + 26 controls / 72 | 72 ✓ | fNIRS / BIDS 1.10 + SNIRF | 725 MB | CC0-1.0 | [прямая загрузка](https://datadryad.org/api/v2/datasets/doi%3A10.5061%2Fdryad.crjdfn3g9/download) | verified-core |
| `z92nw4n73t` | Mendeley v3 | Visual cognitive motivation и recognition | Здоровые взрослые / 16 | 16 ~ | EEG + fNIRS / EDF + CSV | — | CC-BY-4.0 | [Mendeley](https://data.mendeley.com/datasets/z92nw4n73t) | verified-core |
| `luhmann20synhrf-1` | NITRC current | Rest + synthetic HRF; PPG, respiration, BP, accelerometry | Здоровые взрослые / 14 | 14 ~ | fNIRS + physiology / SNIRF | — | BSD | [NITRC](https://www.nitrc.org/projects/luhmann20synhrf/) | partial: доступ через Download Now |
| `luhmann20synhrf-2` | NITRC current | Rest + synthetic HRF; accelerometry | Здоровые взрослые / 14 | 14 ~ | fNIRS + accelerometry / SNIRF | — | BSD | [NITRC](https://www.nitrc.org/projects/luhmann20synhrf/) | partial: доступ через Download Now |
| `REFED` | Hugging Face / REFED 2025 | 15 emotion videos, baseline, continuous valence/arousal и SAM | Здоровые взрослые / 32 | 64 ✓ | EEG + fNIRS / MATLAB MAT + CSV | — | CC-BY-NC-SA-4.0 | [Hugging Face](https://huggingface.co/datasets/REFED2025/REFED-dataset) | verified-core |

## Правила интерпретации

- `verified-core` означает, что версия, N, размер, лицензия и доступ взяты из API/метаданных канонического репозитория. Это не является проверкой научного качества сигналов.
- `partial` означает, что хотя бы одно ключевое поле взято из статьи/вторичного каталога либо отсутствует.
- `metadata-warning` означает противоречивые, шаблонные или явно неполные repository metadata.
- Для OpenNeuro число участников — количество уникальных `subject` IDs в snapshot summary. Это не гарантирует, что у каждого участника есть пригодная fNIRS-запись для каждой задачи.
- Число записей нельзя суммировать как число людей или trials: один человек может дать много session/task/run-записей, а hyperscanning-запись может соответствовать целой диаде.
- OpenNeuro BIDS task labels сохранены в CSV только как источник; нормализованная `paradigm` не должна автоматически выводиться из кодов вроде `AC001`, `MOV003` или `task-nirs`.
- Колонки `features_<group>` перечисляют только положительно подтверждённые признаки. Пустая ячейка не доказывает отсутствие признака в скачиваемом архиве.
- Лицензия статьи, кода и датасета может различаться. В таблице указана лицензия датасета; если она не подтверждена, поле оставлено пустым или помечено «Не указана».

## Конфликты и ограничения

- Удалённые OpenNeuro-дубли `ds004929` и `ds006528` перенаправляют на `ds007420` и `ds006545`; в реестре сохранены только актуальные наборы.
- `ds006673` и `ds006903` имеют почти одинаковую структуру (17 участников, 67 SNIRF), но связь между ними не подтверждена; оба сохранены с предупреждением.
- `ds007477` содержит 36 номинальных SNIRF-путей, но все они ссылаются на один 26-байтный текстовый dummy payload. Валидных raw-записей: 0.
- В `ds004973` ожидаются 240 запусков, но snapshot содержит 222 SNIRF; README сообщает об исключённых/не записанных данных.
- PhysioNet `mental-fnirs` заявляет 14 участников, но публичный file tree содержит 12 полных NIRx stems.
- Для Tufts raw-счётчики равны 87 visual и 53 audio; 68 и 52 — рекомендуемые quality-filtered ML-подвыборки.
- Для `mendeley:377b4ff8p6` статья подтверждает N=12, но Mendeley API не позволил независимо перечислить SNIRF, поэтому count имеет статус `partial`.
- В `ds007738` 223 SNIRF-пути соответствуют 199 уникальным raw-содержимым: 24 пары `longvisualorient`/`videoattend` являются альтернативной разметкой одних файлов.
- REFED теперь опубликован на Hugging Face: N=32, 64 fNIRS MAT-контейнера и 480 размеченных video trials; реестр считает контейнеры, а не trials.

## Способы пакетной загрузки

OpenNeuro:

```bash
openneuro download <dataset_id> <destination_dir>
```

PhysioNet:

```bash
wget -r -N -c -np https://physionet.org/files/<slug>/<version>/
```

Для OpenNeuro CLI могут потребоваться login/API key и `git-annex`/DataLad для annexed-файлов. Конкретные прямые ссылки для остальных источников находятся в колонке `access_url` файла `registry.csv`.
# open_datasets
