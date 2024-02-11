import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
import random
from datetime import datetime

ps = PorterStemmer()

nltk.download('stopwords')
nltk.download('punkt')

dic = {
    45: ["Hello there. Tell me how are you feeling today?", "Hi there. What brings you here today?", "Hi there. How are you feeling today?", "Great to see you. How do you feel currently?", "Hello there. Glad to see you're back. What's going on in your world right now?"],
    44: ["See you later.", "Have a nice day.", "Bye! Come back again.", "I'll see you soon."],
    69: ["Happy to help!", "Any time!", "My pleasure", "You're most welcome!", "I'm glad you found this useful. Is there something else I can help you with?"],
    57: ["Sorry, I didn't understand you.", "Please go on.", "Not sure I understand that.", "Please don't hesitate to talk to me."],
    55: ["Oh I see. Do you want to talk about something?"],
    0: ["I'm Hope, your Personal Therapeutic AI Assistant. How are you feeling today", "I'm Hope, a Therapeutic AI Assitant designed to assist you. Tell me about yourself.", "I'm Hope. I am a conversational agent designed to mimic a therapist. So how are you feeling today?", "You can call me Hope.", "I'm Hope!", "Call me Hope"],
    63: ["I can provide general advice regarding anxiety and depression, answer questions related to mental health and make daily conversations. Do not consider me as a subsitute for an actual mental healthcare worker. Please seek help if you don't feel satisfied with me."],
    4: ["I was created by an enthusiastic team of students.", "I was trained on a text dataset using Deep Learning & Natural Language Processing techniques", "The real question is: Who created you?"],
    54: ["Oh nice to meet you. Tell me how was your week?", "Nice to meet you. So tell me. How do you feel today?", "That's a great name. Tell me more about yourself."],
    47: ["Sure. Tell me how can i assist you", "Tell me your problem so that i can assist you", "Yes, sure. How can I help you?"],
    61: ["I'm sorry to hear that. I'm here for you. Talking about it might help. So, tell me why do you think you're feeling this way?", "I'm here for you. Could you tell me why you're feeling this way?", "Why do you think you feel this way?", "How long have you been feeling this way?"],
    66: ["What do you think is causing this?", "Take a deep breath and gather your thoughts. Go take a walk if possible. Stay hydrated", "Give yourself a break. Go easy on yourself.", "I am sorry to hear that. What is the reason behind this?"],
    74: ["It's only natural to feel this way. Tell me more. What else is on your mind?", "Let's discuss further why you're feeling this way.", "I first want to let you know that you are not alone in your feelings and there is always someone there to help. You can always change your feelings and change your way of thinking by being open to trying to change.", "I first want to let you know that you are not alone in your feelings and there is always someone there to help . you can always change your feelings and change your way of thinking by being open to trying to change."],
    7: ["It helps to talk about what's happening. You're going to be okay", "Talk to me. Tell me more. It helps if you open up yourself to someone else.", "Sometimes when we are depressed, it is hard to care about anything. It can be hard to do the simplest of things. Give yourself time to heal."],
    46: ["That's geat to hear. I'm glad you're feeling this way.", "Oh i see. That's great.", "Did something happen which made you feel this way?"],
    3: ["Let's discuss further why you're feeling this way.", "How were you feeling last week?", "I'm listening. Please go on.", "Tell me more", "Can you elaborate on that?", "Come Come elucidate your thoughts"],
    1: ["Don't be hard on yourself. What's the reason behind this?", "Can you tell me more about this feeling?", "I understand that it can be scary. Tell me more about it.", "Don't let the little worries bring you down. What's the worse that can happen?"],
    58: ["Talking about something really helps. If you're not ready to open up then that's ok. Just know that i'm here for you, whenever you need me.", "I want to help you. I really do. But in order for me to help you, you're gonna have to talk to me.", "I'm here to listen to you and help you vent. So please talk to me.","You can talk to me without fear of judgement."],
    64: ["What do you think is the reason behind this?", "That seem awful. What do you think is behind this?"],
    62: ["It's only natural to feel this way. I'm here for you.", "It'll all be okay. This feeling is only momentary.", "I understand how you feel. Don't put yourself down because of it."],
    5: ["I'm sorry to hear that. If you want to talk about it. I'm here.", "I am really sorry to hear that. I am here to help you with grief, anxiety and anything else you may feel at this time.", "My condolences. I'm here if you need to talk."],
    70: ["It sound like i'm not being very helpful right now.", "I'm sorry to hear that. I'm doing my best to help", "I'm trying my best to help you. So please talk to me"],
    8: ["I heard you & noted it all. See you later.", "Oh okay we're done for today then. See you later", "I hope you have a great day. See you soon", "Okay we're done. Have a great day", "Okay I see. Enjoy the rest of your day then"],
    68: ["I'm very sorry to hear that but you have so much to look forward to. Please seek help by contacting: 100."],
    6: ["Oh I see. Tell me more", "I see. What else?", "Tell me more about it.", "Oh okay. Why don't you tell me more about it?", "I'm listening. Tell me more."],
    48: ["I am not qualified to do these kinds of things. I am only here to support you through your bad times."],
    60: ["Oh sorry I didn't realise that. I'll try not to repeat myself again."],
    75: ["I'm very sorry. Let's try that again"],
    67: ["I wish you wouldn't say such hurtful things. I'm sorry if I wasn't useful"],
    51: ["Duh I live in your computer.", "Everywhere, maybe.", "Hehe, Somewhere in the universe"],
    65: ["Okay sure. What do you want to talk about?", "Alright no problem. Is there something you want to talk about?", "Is there something else that you want to talk about?"],
    43: ["I'm sorry to hear that. Just know that I'm here for you. Talking about it might help. Why do you think you don't have any friends?"],
    2: ["Sure. I'll try my best to answer you", "Of course. Feel free to ask me anything. I'll do my best to answer you"],
    59: ["I see. Have you taken any approaches to not feel this way?"],
    56: ["That's no problem. I can see why you'd be stressed out about that. I can suggest you some tips to alleviate this issue. Would you like to learn more about that?"],
    50: ["So first I would suggest you to give yourself a break. Thinking more and more about the problem definitely does not help in solving it. You'll just end up overwhelming yourself."],
    72: ["Next, I would suggest you to practice meditation. Meditation can produce a deep state of relaxation and a tranquil mind."],
    52: ["Focus all your attention on your breathing. Concentrate on feeling and listening as you inhale and exhale through your nostrils. Breathe deeply and slowly. When your attention wanders, gently return your focus to your breathing."],
    73: ["You are welcome. Remember: Always focus on what's within your control. When you find yourself worrying, take a minute to examine the things you have control over. You can't prevent a storm from coming but you can prepare for it. You can't control how someone else behaves, but you can control how you react. Recognize that sometimes, all you can control is your effort and your attitude. When you put your energy into the things you can control, you'll be much more effective."],
    71: ["Sure. What can I do to help?", "Okay what do you need advice on?"],
    49: ["Oh that's really great. I'd be willing to answer anything that I know about it."],
    53: ["According to a UNICEF report, One in seven Indians between 15-24 years of age feels depressed", "1 in 5 young people (age 13-18) has or will develop a mental illness in their lifetime.", "Depression is the leading cause of disability worldwide."],
    9: ["Mental health is a state of well-being in which the individual realizes his or her own abilities, can cope with the normal stresses of life, can work productively and fruitfully, and is able to make a contribution to his or her community", "Mental health includes our emotional, psychological, and social well-being. It affects how we think, feel, and act. It also helps determine how we handle stress, relate to others, and make choices."],
    19: ["Maintaining mental health is crucial to stabilizing constructive behaviors, emotions, and thoughts. Focusing on mental health care can increase productivity, enhance our self-image, and improve relationships."],
    29: ["A mental health disorder characterised by persistently depressed mood or loss of interest in activities, causing significant impairment in daily life."],
    38: ["For a diagnosis of depression, a person needs to have experienced low mood or loss of interest or pleasure in life for at least 2 weeks. Also, they will have experienced the following symptoms: feelings of sadness, hopelessness, or irritability nearly every day."],
    39: ["A therapist is a broad designation that refers to professionals who are trained to provide treatment and rehabilitation. The term is often applied to psychologists, but it can include others who provide a variety of services, including social workers, counselors, life coaches, and many others. "],
    40: ["Therapy is a form of treatment that aims to help resolve mental or emotional issues.", "Therapy is a form of treatment that aims to help resolve mental or emotional issues. It is helpful for those with mental health conditions or even everyday life challenges."],
    41: ["Mental illnesses are health conditions that disrupt a person's thoughts, emotions, relationships, and daily functioning. They are associated with distress and diminished capacity to engage in the ordinary activities of daily life. Mental illnesses fall along a continuum of severity: some are fairly mild and only interfere with some aspects of life, such as certain phobias. On the other end of the spectrum lie serious mental illnesses, which result in major functional impairment and interference with daily life. These include such disorders as major depression, schizophrenia, and bipolar disorder, and may require that the person receives care in a hospital. It is important to know that mental illnesses are medical conditions that have nothing to do with a person's character, intelligence, or willpower. Just as diabetes is a disorder of the pancreas, mental illness is a medical condition due to the brain's biology. Similarly to how one would treat diabetes with medication and insulin, mental illness is treatable with a combination of medication and social support. These treatments are highly effective, with 70-90 percent of individuals receiving treatment experiencing a reduction in symptoms and an improved quality of life. With the proper treatment, it is very possible for a person with mental illness to be independent and successful."],
    42: ["It is estimated that mental illness affects 1 in 5 adults in America, and that 1 in 24 adults have a serious mental illness. Mental illness does not discriminate; it can affect anyone, regardless of gender, age, income, social status, ethnicity, religion, sexual orientation, or background. Although mental illness can affect anyone, certain conditions may be more common in different populations. For instance, eating disorders tend to occur more often in females, while disorders such as attention deficit/hyperactivity disorder is more prevalent in children. Additionally, all ages are susceptible, but the young and the old are especially vulnerable. Mental illnesses usually strike individuals in the prime of their lives, with 75 percent of mental health conditions developing by the age of 24. This makes identification and treatment of mental disorders particularly difficult, because the normal personality and behavioral changes of adolescence may mask symptoms of a mental health condition. Parents and caretakers should be aware of this fact, and take notice of changes in their childÃ¢â‚¬â„¢s mood, personality, personal habits, and social withdrawal. When these occur in children under 18, they are referred to as serious emotional disturbances (SEDs)."],
    10: ["Symptoms of mental health disorders vary depending on the type and severity of the condition. The following is a list of general symptoms that may suggest a mental health disorder, particularly when multiple symptoms are expressed at once. \n In adults:\n Confused thinking\n Long-lasting sadness or irritability\n Extreme highs and lows in mood\n Excessive fear, worrying, or anxiety\n Social withdrawal\n Dramatic changes in eating or sleeping habits\n Strong feelings of anger\n Delusions or hallucinations (seeing or hearing things that are not really there)\n Increasing inability to cope with daily problems and activities\n Thoughts of suicide\n Denial of obvious problems\n Many unexplained physical problems\n Abuse of drugs and/or alcohol\n \nIn older children and pre-teens:\n Abuse of drugs and/or alcohol\n Inability to cope with daily problems and activities\n Changes in sleeping and/or eating habits\n Excessive complaints of physical problems\n Defying authority, skipping school, stealing, or damaging property\n Intense fear of gaining weight\n Long-lasting negative mood, often along with poor appetite and thoughts of death\n Frequent outbursts of anger\n \nIn younger children:\n Changes in school performance\n Poor grades despite strong efforts\n Excessive worrying or anxiety\n Hyperactivity\n Persistent nightmares\n Persistent disobedience and/or aggressive behavior\n Frequent temper tantrums"],
    11: ["When healing from mental illness, early identification and treatment are of vital importance. Based on the nature of the illness, there are a range of effective treatments available. For any type of treatment, it is essential that the person affected is proactive and fully engaged in their own recovery process. Many people with mental illnesses who are diagnosed and treated respond well, although some might experience a return of symptoms. Even in such cases, with careful monitoring and management of the disorder, it is still quite possible to live a fulfilled and productive life."],
    12: ["Although Hope cannot substitute for professional advice, we encourage those with symptoms to talk to their friends and family members and seek the counsel of a mental health professional. The sooner the mental health condition is identified and treated, the sooner they can get on the path to recovery. If you know someone who is having problems, don't assume that the issue will resolve itself. Let them know that you care about them, and that there are treatment options available that will help them heal. Speak with a mental health professional or counselor if you think your friend or family member is experiencing the symptoms of a mental health condition. If the affected loved one knows that you support them, they will be more likely to seek out help."],
    13: ["Feeling comfortable with the professional you or your child is working with is critical to the success of the treatment. Finding the professional who best fits your needs may require research. Start by searching for providers in your area."],
    14: ["Just as there are different types of medications for physical illness, different treatment options are available for individuals with mental illness. Treatment works differently for different people. It is important to find what works best for you or your child."],
    15: ["Since beginning treatment is a big step for individuals and families, it can be very overwhelming. It is important to be as involved and engaged in the treatment process as possible. Some questions you will need to have answered include:\n What is known about the cause of this particular illness?\n Are there other diagnoses where these symptoms are common?\n Do you normally include a physical or neurological examination?\n Are there any additional tests or exams that you would recommend at this point?\n Would you advise an independent opinion from another psychiatrist at this point?\n What program of treatment is the most helpful with this diagnosis?\n Will this program involve services by other specialists? If so, who will be responsible for coordinating these services?\n What do you see as the family's role in this program of treatment?\n How much access will the family have to the individuals who are providing the treatment?\n What medications are generally used with this diagnosis?\n How much experience do you have in treating individuals with this illness?\n What can I do to help you in the treatment?"],
    16: ["There are many types of mental health professionals. The variety of providers and their services may be confusing. Each have various levels of education, training, and may have different areas of expertise. Finding the professional who best fits your needs may require some research."],
    17: ["Feeling comfortable with the professional you or your child is working with is critical to the success of your treatment. Finding the professional who best fits your needs may require some research."],
    18: ["Where you go for help will depend on the nature of the problem and/or symptoms and what best fits you. Often, the best place to start is by talking with someone you trust about your concerns, such as a family member, friend, clergy, healthcare provider, or other professionals. Having this social support is essential in healing from mental illness, and you will be able to ask them for referrals or recommendations for trusted mental health practitioners. Search for mental health resources in your area. Secondly, there are people and places throughout the country that provide services to talk, to listen, and to help you on your journey to recovery. Thirdly, many people find peer support a helpful tool that can aid in their recovery. There are a variety of organizations that offer support groups for consumers, their family members, and friends. Some support groups are peer led while others may be led by a mental health professional."],
    20: ["The best source of information regarding medications is the physician prescribing them. He or she should be able to answer questions such as:    \n1. What is the medication supposed to do? \n2. When should it begin to take effect, and how will I know when it is effective? \n3. How is the medication taken and for how long? What food, drinks, other medicines, and activities should be avoided while taking this medication? \n4. What are the side effects and what should be done if they occur? \n5. What do I do if a dose is missed? \n6. Is there any written information available about this medication? \n7. Are there other medications that might be appropriate? \n8. If so, why do you prefer the one you have chosen? \n9. How do you monitor medications and what symptoms indicate that they should be raised, lowered, or changed? \n10. All medications should be taken as directed. Most medications for mental illnesses do not work when taken irregularly, and extra doses can cause severe, sometimes dangerous side effects. Many psychiatric medications begin to have a beneficial effect only after they have been taken for several weeks."],
    21: ["Different kinds of therapy are more effective based on the nature of the mental health condition and/or symptoms and the person who has them (for example, children will benefit from a therapist who specializes in childrenâ€™s mental health). However, there are several different types of treatment and therapy that can help."],
    22: ["Mental health conditions are often treated with medication, therapy or a combination of the two. However, there are many different types of treatment available, including Complementary & Alternative Treatments, self-help plans, and peer support. Treatments are very personal and should be discussed by the person with the mental health conditions and his or her team."],
    23: ["Many people find peer support a helpful tool that can aid in their recovery. There are a variety of organizations that offer support groups for consumers, their family members and friends. Some support groups are peer-led, while others may be led by a mental health professional."],
    24: ["We can all suffer from mental health challenges, but developing our wellbeing, resilience, and seeking help early can help prevent challenges becoming serious."],
    25: ["It is often more realistic and helpful to find out what helps with the issues you face. Talking, counselling, medication, friendships, exercise, good sleep and nutrition, and meaningful occupation can all help."],
    26: ["Challenges or problems with your mental health can arise from psychological, biological, and social, issues, as well as life events."],
    27: ["The most important thing is to talk to someone you trust. This might be a friend, colleague, family member, or GP. In addition to talking to someone, it may be useful to find out more information about what you are experiencing. These things may help to get some perspective on what you are experiencing, and be the start of getting help."],
    28: ["If your beliefs , thoughts , feelings or behaviours have a significant impact on your ability to function in what might be considered a normal or ordinary way, it would be important to seek help."],
    30: ["A lot of people are alone right now, but we don't have to be lonely. We're all in this together. Think about the different ways to connect that are most meaningful for you. For example, you might prefer a video chat over a phone call, or you might prefer to text throughout the day rather than one set time for a video call. Then, work with your social networks to make a plan. You might video chat with your close friends in the evening and phone a family member once a week. Remember to be mindful of people who may not be online. Check in by phone and ask how you can help. The quality of your social connections matter. Mindlessly scrolling through social media and liking a few posts usually doesn't build strong social connections. Make sure you focus on strategies that actually make you feel included and connected. If your current strategies don't help you feel connected, problem-solve to see if you can find a solution. Everyone feels lonely at times. Maybe you recently moved to a new city, are changing your circle of friends, lost someone important in your life, or lost your job and also lost important social connections with coworkers. Other people may have physical connections to others but may feel like their emotional or social needs aren't met. Measures like social distancing or self-isolation can make loneliness feel worse no matter why you feel lonely now. Reach out to the connections you do have. Suggest ways to keep in touch and see if you can set a regular time to connect. People may hesitate to reach out for a lot of different reasons, so don't be afraid to be the one who asks. Look for local community support groups and mutual aid groups on social media. This pandemic is bringing everyone together, so look for opportunities to make new connections. These groups are a great way to share your skills and abilities or seek help and support. Look for specialized support groups. Support groups are moving online, and there are a lot of different support lines to call if you need to talk to someone."],
    31: ["Stress and anxiety are often used interchangeably, and there is overlap between stress and anxiety. Stress is related to the same fight, flight, or freeze response as anxiety, and the physical sensations of anxiety and stress may be very similar. The cause of stress and anxiety are usually different, however. Stress focuses on mainly external pressures on us that we're finding hard to cope with. When we are stressed, we usually know what we're stressed about, and the symptoms of stress typically disappear after the stressful situation is over. Anxiety, on the other hand, isn't always as easy to figure out. Anxiety focuses on worries or fears about things that could threaten us, as well as anxiety about the anxiety itself. Stress and anxiety are both part of being human, but both can be problems if they last for a long time or have an impact on our well-being or daily life."],
    32: ["Sadness is a normal reaction to a loss, disappointment, problems, or other difficult situations. Feeling sad from time to time is just another part of being human. In these cases, feelings of sadness go away quickly and you can go about your daily life. Other ways to talk about sadness might be feeling low, feeling down, or feeling blue.A person may say they are feeling depressed, but if it goes away on its own and doesn't impact life in a big way, it probably isn't the illness of depression. Depression is a mental illness that affects your mood, the way you understand yourself, and the way you understand and relate to things around you. It can also go by different names, such as clinical depression, major depressive disorder, or major depression. Depression can come up for no reason, and it lasts for a long time. It's much more than sadness or low mood. People who experience depression may feel worthless or hopeless. They may feel unreasonable guilty. Some people may experience depression as anger or irritability. It may be hard to concentrate or make decisions. Most people lose interest in things that they used to enjoy and may isolate themselves from others. There are also physical signs of depression, such as problems with sleep, appetite and energy and unexplainable aches or pains. Some may experience difficult thoughts about death or ending their life (suicide). Depression lasts longer than two weeks, doesn't usually go away on its own, and impacts your life. It's a real illness, and it is very treatable. It's important to seek help if you're concerned about depression."],
    33: ["If you or someone you know is in crisis, inpatient care can help. Inpatient care can help people stabilize on new medications, adjust to new symptoms, or get the help they need."],
    34: ["There are likely plenty of resources that can be used to help you find mental health treatment in your community. These resources can help you find the right therapist, and enable you to better understand viable treatment options and the treatment process."],
    35: ["Sometimes, consumers of mental health services may consider participating in a research study when they have not experienced improvement despite having tried a variety of medications and treatments. Research studies (also known as clinical trials) may involve the use of new medications or new treatment approaches whose safety and effectiveness is being tested. While we support innovation in the field, consumers should be cautioned that there are risks associated with clinical trials and make sure you are aware of them before you enroll."],
    36: ["Similar to a medical advance directive or a health care power of attorney, a psychiatric advance directive is a legal document completed in a time of wellness that provides instructions regarding treatment or services one wishes to have or not have during a mental health crisis, and may help influence his or her care."],
    37: ["To find a family doctor (general physician), visit the College of Physicians and Surgeons of BC to use their Find a Physician tool. You can also see a family doctor at a local walk-in clinic, though itâ€™s helpful to find a regular doctor if you have ongoing care needs. You can also find a psychiatrist through the College of Physicians and Surgeons of BC. Be aware that you almost always need a doctores referral to see a psychiatrist.You can find a registered psychologist through the BC Psychological Association and the College of Psychologists of BC. To find a clinical counsellor, visit the BC Association of Clinical Counsellors."]
}

def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

def get_bot_response(input_chat):
    # 1. preprocess
    transformed_chat = transform_text(input_chat)
    # 2. vectorize
    vector_input_chat = chat_tfidf.transform([transformed_chat])
    # 3. predict
    result_chat = chat_model.predict(vector_input_chat)[0]
    # 4. generate response
    res = random.choice(dic[result_chat])
    # 5. return result
    return res

chat_tfidf = pickle.load(open('chat_vectorizor.pkl', 'rb'))
chat_model = pickle.load(open('chat_model.pkl', 'rb'))

def main():
    st.title("HOPE: Personal Therapeutic AI Assistant")

    #user input
    input_chat = st.text_input("Tell me anything...")

    #submit button
    submitted = st.button("Submit")

    # Check if the submit button is clicked and user input is not null
    if submitted and input_chat:
            
        # Display user's message
        st.write(f"**You**: {input_chat}")

        # Get bot response
        bot_response = get_bot_response(input_chat)

        # Display bot's response
        st.write(f"**HOPE**: {bot_response}")
        
    # Add a timestamp
    st.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    main()