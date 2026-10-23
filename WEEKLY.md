# Weekly poster job (every Sunday)

This repo holds the Instagram posters for **Anand Agro Agencies** (शेलगाव (वांगी), ता. करमाळा,
phone 9284188428, सोम–शनि सकाळी १० ते रात्री ८). Owner: Nilesh Pote, who reads Marathi and is
not technical. Write every message to him in simple Marathi.

The posters are picked up by the Make scenario "Anand Agro Instagram Auto-Post" (id 8101960),
which runs daily at 19:30 IST and posts the row of the Google Sheet whose date is today **and**
whose Status is `Ready`. When column L holds a `raw.githubusercontent.com` link, Make uses that
image; otherwise it uses the Drive file `Day-NN.*` from the media folder.

## Where things are

| what | where |
| --- | --- |
| Content calendar | Google Sheet `11Xovx256nrljGFou2UZ-7QqHOhCqzoOnTH5hQiIeJNY`, tab `Content Calendar` |
| Columns | A Day, B Date (`DD-MMM-YYYY`, e.g. `22-Nov-2026`), C Weekday (Marathi), D Post Time (`19:30`), E Pillar, F Format, G Topic, H Caption, I Hashtags, J Visual, K CTA, L Image URL, M Status, N Posted Link |
| Media folder (his own photos) | Drive folder `1yfqeeTXTYe_W-UT0kHnv2Vgob-eSjU5W` |
| Poster renderer | `render.py` here; specs in `specs/<first-date>.json`; output `posters/Day-NN.jpg` |
| Poster URL | `https://raw.githubusercontent.com/nileshpote47-ui/anandagro-posters/main/posters/Day-NN.jpg` |

Weekday names: सोम मंगळ बुध गुरु शुक्र शनि रवि.

## The job

1. Read the whole sheet. Find the last date. The horizon is **tomorrow through tomorrow + 13 days**.
2. For every date in the horizon that has no row, add one row (Day = previous max + 1):
   - D `19:30`, F `Post`, J `GitHub poster (आपोआप बनवलेलं)`, M `Draft`, L = the poster URL above.
   - Pillars across each week: Education ×3, Offer ×1, Trust ×1, Engagement ×1, Product ×1.
   - Topic: practical, seasonal for Solapur district (rabi Oct–Feb, summer Mar–May, kharif Jun–Sep),
     banana (केळी) often. Read every existing topic first and do not repeat one.
   - Caption (H): Marathi, under ~450 characters, first line is the hook, numbered points with 1️⃣ 2️⃣ 3️⃣,
     one clear ask. Offer/Product rows end with
     `📞 9284188428 | 📍 शेलगाव (वांगी), करमाळा | सोम–शनि, सकाळी १० ते रात्री ८`.
   - Hashtags (I), exactly one of these two sets:
     banana rows `#केळीशेती #G9केळी #टिश्यूकल्चर #करमाळा #आनंदअॅग्रो`,
     all others `#शेती #शेतकरी #करमाळा #सोलापूर #आनंदअॅग्रो`.
3. Write `specs/<first-new-date>.json` for the new rows (see `render.py` for the four kinds:
   tip, offer, question, message) and run `python3 render.py specs/<file>.json`. Fix any OVERFLOW
   by shortening text. Open every new JPEG and look at it before pushing.
4. Commit and push to `main`, then check each new poster URL returns HTTP 200 with curl.
5. Only after the push succeeds, write the new rows to the sheet.
6. Check the Make scenario is active and read its last executions; explain any error in plain Marathi.
7. Send Nilesh one Marathi message: the new topics with dates, which of the next 7 days are still
   `Draft`, and a reminder that only `Ready` rows get posted. Attach a contact sheet of the new posters.

## Content rules (these protect the shop)

- No pesticide or fertiliser doses, no brand names of chemicals. Say `लेबलवरील प्रमाणानुसार`.
- No yield, income or disease-cure guarantees. No health claims.
- Do not invent products, prices or offers. The shop sells seeds, fertilisers, crop-protection
  products and banana tissue-culture plants (G9), with a free crop and spray schedule and free advice.
- No real farmer's name, photo or testimonial unless Nilesh gave it.

## Never

- Never set a Status to `Ready`. Only Nilesh does that.
- Never change a row whose date is today or earlier, or any row marked `Posted`.
- Never edit, run or switch off the Make scenario. Never post to Instagram.
- Never delete files in Drive or in this repo's history.
